#include <TinyMLShield.h>

#include <PDM.h>
#include <voice_detection_inferencing.h>

// wifi_upload, A6 for TX, A7 for RX
UART softSerial1(analogPinToPinName(6), analogPinToPinName(7), NC, NC);



// audio buffers, pointers and selectors
typedef struct {
  int16_t *buffer;
  uint8_t buf_ready;
  uint32_t buf_count;
  uint32_t n_samples;
} inference_t;

static inference_t inference;
static signed short sampleBuffer[2048];
static bool debug_nn = false; // Set this to true to see e.g. features generated from the raw signal

// camera flags
bool commandRecv = false; // flag used for indicating receipt of commands from serial port
bool liveFlag = false; // flag as true to live stream raw camera bytes, set as false to take single images on command
bool captureFlag = true;

// Image buffer
byte image[320 * 240 * 2]; // QVGA: 320x240 x 2 bytes per pixel (RGB565)
long long bytesPerFrame;

// setup
void setup() {
  Serial.begin(115200);
  while (!Serial);
  softSerial1.begin(115200);
  while (!softSerial1);

  // softSerial1.println("softSerial test");
  initializeShield();

  // initialize the microphone
  if (microphone_inference_start(EI_CLASSIFIER_RAW_SAMPLE_COUNT) == false) {
    ei_printf("ERR: Could not allocate audio buffer (size %d), this could be due to the window length of your model\r\n", EI_CLASSIFIER_RAW_SAMPLE_COUNT);
    return;
  }

  // initialize the OV7675 camera
  if (!Camera.begin(QVGA, RGB565, 1, OV7675)) {
    Serial.println("Failed to initialize camera");
    while (1);
  }
  bytesPerFrame = Camera.width() * Camera.height() * Camera.bytesPerPixel();

  if (microphone_inference_start(EI_CLASSIFIER_RAW_SAMPLE_COUNT) == false) {
        ei_printf("ERR: Could not allocate audio buffer (size %d), this could be due to the window length of your model\r\n", EI_CLASSIFIER_RAW_SAMPLE_COUNT);
        return;
    }

  //Serial.println("Welcome to the OV7675 test\n");
  //Serial.println("Available commands:\n");
  //Serial.println("single - take a single image and print out the hexadecimal for each pixel (default)");
  //Serial.println("live - the raw bytes of images will be streamed live over the serial port");
  //Serial.println("capture - when in single mode, initiates an image capture");


  //wifi init
  //Serial.begin(115200);
  // Serial1.begin(115200);
  // delay(3000);
  // Serial.println("wifi STA TCP test begin!");
  // Serial1.println("AT+CIPSTART=\"TCP\",\"192.168.124.7\",8080");
  // Serial.println("AT+CIPSTART=\"TCP\",\"192.168.124.7\",8080,WAITING...");
  // delay(5000);

  // Serial1.println("AT+CIPMODE=1");
  // Serial.println("AT+CIPMODE=1,WAITING...");
  // delay(2000);

  // Serial1.println("AT+CIPSEND");
  // Serial.println("AT+CIPSEND,WAITING...");
  // delay(2000);



  // initialize esp-01

  // softSerial1.listen();
  delay(3000);
  softSerial1.println("AT+CIPSTART=\"TCP\",\"192.168.124.7\",8090");
  delay(5000);

  softSerial1.println("AT+CIPMODE=1");
  delay(2000);

  softSerial1.println("AT+CIPSEND");
  delay(2000);
}

void loop() {
  int i = 0;
  String command;

  bool clicked = readShieldButton();
  if (clicked) {
    if (!liveFlag) {
      if (!captureFlag) {
        captureFlag = true;
      }
    }
  }

  

  // noise classfication and upload
  Serial.println("noise classfication and upload");
  delay(2000);

  bool m = microphone_inference_record();
  if (!m) {
    ei_printf("ERR: Failed to record audio...\n");
    return;
  }
  
  signal_t signal;
  signal.total_length = EI_CLASSIFIER_RAW_SAMPLE_COUNT;
  signal.get_data = &microphone_audio_signal_get_data;
  ei_impulse_result_t result = { 0 };

  EI_IMPULSE_ERROR r = run_classifier(&signal, &result, debug_nn);
  if (r != EI_IMPULSE_OK) {
    ei_printf("ERR: Failed to run classifier (%d)\n", r);
    return;
  }
  //  // print the predictions
  //  ei_printf("Predictions ");
  //  ei_printf("(DSP: %d ms., Classification: %d ms., Anomaly: %d ms.)",
  //            result.timing.dsp, result.timing.classification, result.timing.anomaly);
  //  ei_printf(": \n");
  for (size_t ix = 0; ix < EI_CLASSIFIER_LABEL_COUNT; ix++) {
    ei_printf("%s: %.5f\n", result.classification[ix].label, result.classification[ix].value);
  }
  for (size_t ix = 0; ix < EI_CLASSIFIER_LABEL_COUNT; ix++) {
    softSerial1.print(result.classification[ix].value);

    if (ix != EI_CLASSIFIER_LABEL_COUNT - 1) {
      softSerial1.print(", ");
    }
  }
  softSerial1.print("; ");// ";" to split noise and photo
#if EI_CLASSIFIER_HAS_ANOMALY == 1
  ei_printf("    anomaly score: %.3f\n", result.anomaly);
#endif

  // photo capture and upload
  Serial.println("photo capture and upload");
  if (captureFlag) {
    captureFlag = false;
    Camera.readFrame(image);
    //Serial.println("\nImage data will be printed out in 3 seconds...");
    delay(3000);
    //      for (int i = 0; i < bytesPerFrame - 1; i += 2) {
    //        Serial.print("0x");
    //        Serial.print(image[i+1], HEX);
    //        Serial.print(image[i], HEX);
    //        if (i != bytesPerFrame - 2) {
    //          Serial.print(", ");
    //        }
    //      }
    //      Serial.println();
    Serial.println("uploading photo...");

    //wifi upload
    for (int i = 0; i < bytesPerFrame - 1; i += 2) {
      softSerial1.print("0x");
      softSerial1.print(image[i + 1], HEX);
      softSerial1.print(image[i], HEX);
      if (i != bytesPerFrame - 2) {
        softSerial1.print(", ");
      }
    }
    // "\n" for once upload
    softSerial1.println();
    captureFlag = true;

    //time interval
    delay(5000);//20s一次

  }
}

// noise detection lib
/**
   @brief      PDM buffer full callback
               Get data and call audio thread callback
*/
static void pdm_data_ready_inference_callback(void)
{
  int bytesAvailable = PDM.available();

  // read into the sample buffer
  int bytesRead = PDM.read((char *)&sampleBuffer[0], bytesAvailable);

  if (inference.buf_ready == 0) {
    for (int i = 0; i < bytesRead >> 1; i++) {
      inference.buffer[inference.buf_count++] = sampleBuffer[i];

      if (inference.buf_count >= inference.n_samples) {
        inference.buf_count = 0;
        inference.buf_ready = 1;
        break;
      }
    }
  }
}

/**
   @brief      Init inferencing struct and setup/start PDM

   @param[in]  n_samples  The n samples

   @return     { description_of_the_return_value }
*/
static bool microphone_inference_start(uint32_t n_samples)
{
  inference.buffer = (int16_t *)malloc(n_samples * sizeof(int16_t));

  if (inference.buffer == NULL) {
    return false;
  }

  inference.buf_count  = 0;
  inference.n_samples  = n_samples;
  inference.buf_ready  = 0;

  // configure the data receive callback
  PDM.onReceive(&pdm_data_ready_inference_callback);

  PDM.setBufferSize(4096);

  // initialize PDM with:
  // - one channel (mono mode)
  // - a 16 kHz sample rate
  if (!PDM.begin(1, EI_CLASSIFIER_FREQUENCY)) {
    ei_printf("Failed to start PDM!");
    microphone_inference_end();

    return false;
  }

  // set the gain, defaults to 20
  PDM.setGain(127);

  return true;
}

/**
   @brief      Wait on new data

   @return     True when finished
*/
static bool microphone_inference_record(void)
{
  inference.buf_ready = 0;
  inference.buf_count = 0;

  while (inference.buf_ready == 0) {
    delay(10);
  }

  return true;
}

/**
   Get raw audio signal data
*/
static int microphone_audio_signal_get_data(size_t offset, size_t length, float *out_ptr)
{
  numpy::int16_to_float(&inference.buffer[offset], out_ptr, length);

  return 0;
}

/**
   @brief      Stop PDM and release buffers
*/
static void microphone_inference_end(void)
{
  PDM.end();
  free(inference.buffer);
}

#if !defined(EI_CLASSIFIER_SENSOR) || EI_CLASSIFIER_SENSOR != EI_CLASSIFIER_SENSOR_MICROPHONE
#error "Invalid model for current sensor."
#endif
