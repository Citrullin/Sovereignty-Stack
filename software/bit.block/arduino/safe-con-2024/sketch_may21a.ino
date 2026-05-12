#include <Adafruit_NeoPixel.h>
#include <MD_YX5300.h>

#define DEBUG true
#include <Arduino.h>
#include "Thing.h"
#include "WebThingAdapter.h"

#define PIN_BASE 32 
#define NUMPIXELS_BASE 40

#define PIN_INTERNAL 16
#define NUMPIXELS_INTERNAL 4


const uint8_t VOICE_RX = 39;      
const uint8_t VOICE_TX = 19;

const uint8_t MP3_RX = 36;
const uint8_t MP3_TX = 17;

#define BASE_COLOR_BUFFER_SIZE 512
#define HEAD_COLOR_BUFFER_SIZE 512
#define MOON_COLOR_BUFFER_SIZE 512

#define SOUND_BUFFER_SIZE 512

const char *ssid = "WebOfThingsHub";
const char *password = "PASSWORD";

#define USE_SOFTWARESERIAL 0
#define MP3Stream Serial1

#define Console Serial      // aliasing serial communication w/ IDE 

#ifdef DEBUG
#define PRINT(s,v)    { Console.print(F(s)); Console.print(v); }
#define PRINTX(s,v)   { Console.print(F(s)); Console.print(v, HEX); }
#define PRINTS(s)     { Console.print(F(s)); }
#else
#define PRINT(s,v)    
#define PRINTX(s,v)   
#define PRINTS(s)     
#endif

struct mp3_information {
  uint8_t index;
  uint16_t time;
};

struct mp3_state{
  uint16_t index;
  bool last_successful;
  uint16_t last_chip_response;
  unsigned long previous_time;
  uint16_t current_repeat;
  uint16_t max_repeat;
  uint16_t max_index;
  uint16_t item_amount;
  bool stop;
};

struct mp3_information sound_buffer[SOUND_BUFFER_SIZE];
struct mp3_state mp3_sound_state;
struct mp3_information *previous_mp3_sound;
struct mp3_information *current_mp3_sound;

void cbResponse(const MD_YX5300::cbData *status){
  
  PRINTS("\n");
  mp3_sound_state.last_chip_response = status->code;
  switch (status->code)
  {
  case MD_YX5300::STS_FILE_END:   // track has ended
    PRINTS("STS_FILE_END");
    break;

  case MD_YX5300::STS_TF_INSERT:  // card has been inserted
    PRINTS("STS_TF_INSERT"); 
    break;

  case MD_YX5300::STS_TF_REMOVE:  // card has been removed
    PRINTS("STS_TF_REMOVE"); 
    break;

  case MD_YX5300::STS_PLAYING:   // current track index 
    PRINTS("STS_PLAYING");    
    break;

  case MD_YX5300::STS_FLDR_FILES: // number of files in the folder
    PRINTS("STS_FLDR_FILES"); 
    break;

  // unhandled cases - used for debug only
  case MD_YX5300::STS_VOLUME:     PRINTS("STS_VOLUME");     break;
  case MD_YX5300::STS_TOT_FILES:  PRINTS("STS_TOT_FILES");  break;
  case MD_YX5300::STS_ERR_FILE:   PRINTS("STS_ERR_FILE");   break;
  case MD_YX5300::STS_ACK_OK:     PRINTS("STS_ACK_OK");     break;
  case MD_YX5300::STS_INIT:       PRINTS("STS_INIT");       break;
  case MD_YX5300::STS_STATUS:     PRINTS("STS_STATUS");     break;
  case MD_YX5300::STS_EQUALIZER:  PRINTS("STS_EQUALIZER");  break;
  case MD_YX5300::STS_TOT_FLDR:   PRINTS("STS_TOT_FLDR");   break;
  default: PRINTX("STS_??? 0x", status->code); break;
  }

  PRINTX(", 0x", status->data);
}

Adafruit_NeoPixel pixels(NUMPIXELS_BASE, PIN_BASE, NEO_GRB + NEO_KHZ800);
Adafruit_NeoPixel pixelsExternal(PIN_INTERNAL, PIN_INTERNAL, NEO_GRB + NEO_KHZ800);
MD_YX5300 mp3(MP3Stream);

ThingActionObject *base_light_action_generator(DynamicJsonDocument *);
ThingActionObject *moon_light_action_generator(DynamicJsonDocument *);
ThingActionObject *head_light_action_generator(DynamicJsonDocument *);
ThingActionObject *sound_action_generator(DynamicJsonDocument *);
ThingActionObject *stop_sound_action_generator(DynamicJsonDocument *);
WebThingAdapter *adapter;

const char *bitBlockTypes[] = {"BindBitBlock", nullptr};
ThingDevice bitBlock("bit_block", "bind.systems bit.block", bitBlockTypes);

StaticJsonDocument<2084> baseLightInput;
JsonObject baseLightInputObj = baseLightInput.to<JsonObject>();
ThingAction baseLightAction("base_light", "Light up the base", "RGB light",
                 "baseLightAction", &baseLightInputObj, base_light_action_generator);

StaticJsonDocument<2084> moonLightInput;
JsonObject moonLightInputObj = moonLightInput.to<JsonObject>();
ThingAction moonLightAction("moon_light", "Light up the moon", "RGB light",
                 "moonLightAction", &moonLightInputObj, moon_light_action_generator);

StaticJsonDocument<2084> headLightInput;
JsonObject headLightInputObj = headLightInput.to<JsonObject>();
ThingAction headLightAction("head_light", "Light up the head", "RGB light",
                 "headLightAction", &headLightInputObj, head_light_action_generator);

StaticJsonDocument<512> soundInput;
JsonObject soundInputObj = soundInput.to<JsonObject>();
ThingAction soundAction("sound", "play a sound", "Sound playing",
                 "soundAction", &soundInputObj, sound_action_generator);

StaticJsonDocument<512> stopSoundInput;
JsonObject stopSoundtInputObj = stopSoundInput.to<JsonObject>();
ThingAction stopSoundAction("stop_sound", "stop playing", "stop playing a sound",
                 "stopSoundAction", &stopSoundtInputObj, stop_sound_action_generator);


void create_base_light_input(){
  baseLightInputObj["type"] = "object";
    JsonObject baseLightInputProperties =
      baseLightInputObj.createNestedObject("properties");
  JsonObject baseLightRepeatInput =
      baseLightInputProperties.createNestedObject("repeat");
  baseLightRepeatInput["type"] = "integer";


  JsonObject dataInput =
      baseLightInputProperties.createNestedObject("data");

    dataInput["type"] = "array";
      JsonObject dataInputItems =
        dataInput.createNestedObject("items");

      dataInputItems["type"] = "array";
        JsonArray dataItemsInput = 
         dataInputItems.createNestedArray("items");

        StaticJsonDocument<250> keepDoc;
        JsonObject keepObj = keepDoc.to<JsonObject>();
        keepObj["type"] = "boolean";
        keepObj["title"] = "keep";
        dataItemsInput.add(keepObj);

        StaticJsonDocument<250> indexDoc;
        JsonObject indexObj = indexDoc.to<JsonObject>();
        indexObj["type"] = "integer";
        indexObj["title"] = "index";
        indexObj["maximum"] = 40;
        dataItemsInput.add(indexObj);

        StaticJsonDocument<250> timeDoc;
        JsonObject timeObj = timeDoc.to<JsonObject>();
        timeObj["type"] = "integer";
        timeObj["title"] = "time";
        timeObj["maximum"] = 10000;
        dataItemsInput.add(timeObj);

        StaticJsonDocument<250> redDoc;
        JsonObject redObj = redDoc.to<JsonObject>();
        redObj["type"] = "integer";
        redObj["title"] = "red";
        redObj["maximum"] = 255;
        dataItemsInput.add(redObj);

        StaticJsonDocument<250> greenDoc;
        JsonObject greenObj = greenDoc.to<JsonObject>();
        greenObj["type"] = "integer";
        greenObj["title"] = "green";
        greenObj["maximum"] = 255;
        dataItemsInput.add(greenObj);

        StaticJsonDocument<50> blueDoc;
        JsonObject blueObj = blueDoc.to<JsonObject>();
        blueObj["type"] = "integer";
        blueObj["title"] = "blue";
        blueObj["maximum"] = 255;
        dataItemsInput.add(blueObj);


  bitBlock.addAction(&baseLightAction);
}

void create_moon_light_input(){
  moonLightInputObj["type"] = "object";
    JsonObject moonLightInputProperties =
      moonLightInputObj.createNestedObject("properties");
  JsonObject moonLightRepeatInput =
      moonLightInputProperties.createNestedObject("repeat");
  moonLightRepeatInput["type"] = "integer";


  JsonObject dataInput =
      moonLightInputProperties.createNestedObject("data");

    dataInput["type"] = "array";
      JsonObject dataInputItems =
        dataInput.createNestedObject("items");

      dataInputItems["type"] = "array";
        JsonArray dataItemsInput = 
         dataInputItems.createNestedArray("items");

        StaticJsonDocument<250> timeDoc;
        JsonObject timeObj = timeDoc.to<JsonObject>();
        timeObj["type"] = "integer";
        timeObj["title"] = "time";
        timeObj["maximum"] = 10000;
        dataItemsInput.add(timeObj);

        StaticJsonDocument<250> redDoc;
        JsonObject redObj = redDoc.to<JsonObject>();
        redObj["type"] = "integer";
        redObj["title"] = "red";
        redObj["maximum"] = 255;
        dataItemsInput.add(redObj);

        StaticJsonDocument<250> greenDoc;
        JsonObject greenObj = greenDoc.to<JsonObject>();
        greenObj["type"] = "integer";
        greenObj["title"] = "green";
        greenObj["maximum"] = 255;
        dataItemsInput.add(greenObj);

        StaticJsonDocument<250> blueDoc;
        JsonObject blueObj = blueDoc.to<JsonObject>();
        blueObj["type"] = "integer";
        blueObj["title"] = "blue";
        blueObj["maximum"] = 255;
        dataItemsInput.add(blueObj);


  bitBlock.addAction(&moonLightAction);
}

void create_head_light_input(){
  headLightInputObj["type"] = "object";
    JsonObject headLightInputProperties =
      headLightInputObj.createNestedObject("properties");
  JsonObject headLightRepeatInput =
      headLightInputProperties.createNestedObject("repeat");
  headLightRepeatInput["type"] = "integer";


  JsonObject dataInput =
      headLightInputProperties.createNestedObject("data");

    dataInput["type"] = "array";
      JsonObject dataInputItems =
        dataInput.createNestedObject("items");

      dataInputItems["type"] = "array";
        JsonArray dataItemsInput = 
         dataInputItems.createNestedArray("items");

        StaticJsonDocument<250> timeDoc;
        JsonObject timeObj = timeDoc.to<JsonObject>();
        timeObj["type"] = "integer";
        timeObj["title"] = "time";
        timeObj["maximum"] = 10000;
        dataItemsInput.add(timeObj);

        StaticJsonDocument<250> redDoc;
        JsonObject redObj = redDoc.to<JsonObject>();
        redObj["type"] = "integer";
        redObj["title"] = "red";
        redObj["maximum"] = 255;
        dataItemsInput.add(redObj);

        StaticJsonDocument<250> greenDoc;
        JsonObject greenObj = greenDoc.to<JsonObject>();
        greenObj["type"] = "integer";
        greenObj["title"] = "green";
        greenObj["maximum"] = 255;
        dataItemsInput.add(greenObj);

        StaticJsonDocument<250> blueDoc;
        JsonObject blueObj = blueDoc.to<JsonObject>();
        blueObj["type"] = "integer";
        blueObj["title"] = "blue";
        blueObj["maximum"] = 255;
        dataItemsInput.add(blueObj);


  bitBlock.addAction(&headLightAction);
}

void create_sound_input(){
  soundInputObj["type"] = "object";
    JsonObject soundInputProperties =
      soundInputObj.createNestedObject("properties");
  JsonObject soundRepeatInput =
      soundInputProperties.createNestedObject("repeat");
  soundRepeatInput["type"] = "integer";


  JsonObject dataInput =
      soundInputProperties.createNestedObject("data");

    dataInput["type"] = "array";
      JsonObject dataInputItems =
        dataInput.createNestedObject("items");

      dataInputItems["type"] = "array";
        JsonArray dataItemsInput = 
         dataInputItems.createNestedArray("items");

        StaticJsonDocument<250> indexDoc;
        JsonObject indexObj = indexDoc.to<JsonObject>();
        indexObj["type"] = "integer";
        indexObj["title"] = "index";
        indexObj["maximum"] = 40;
        dataItemsInput.add(indexObj);

        StaticJsonDocument<250> timeDoc;
        JsonObject timeObj = timeDoc.to<JsonObject>();
        timeObj["type"] = "integer";
        timeObj["title"] = "time";
        timeObj["maximum"] = 10000;
        dataItemsInput.add(timeObj);

  bitBlock.addAction(&soundAction);
}

void create_stop_sound_input(){
  bitBlock.addAction(&stopSoundAction);
}

void setup_wifi(){
  Serial.println("");
  Serial.print("Connecting to \"");
  Serial.print(ssid);
  Serial.println("\"");
#if defined(ESP8266) || defined(ESP32)
  WiFi.mode(WIFI_STA);
#endif
  WiFi.begin(ssid, password);
  
  bool blink = true;
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");

    if(blink){
      pixels.setPixelColor(20, pixels.Color(255, 0, 0));
      pixels.show(); 
    }else{
      pixels.setPixelColor(20, pixels.Color(0, 0, 0));
      pixels.show(); 
    }
 
    blink = !blink;
  }
  pixels.setPixelColor(20, pixels.Color(0, 0, 0));
  pixels.show(); 

  Serial.println("");
  Serial.print("Connected to ");
  Serial.println(ssid);
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());
}

void init_wot_config(){
  adapter = new WebThingAdapter("matrix-display", WiFi.localIP());
  bitBlock.description = "bind.systems bit.block web of things development kit";
}

uint8_t vol;
void setup_mp3(){
  MP3Stream.begin(MD_YX5300::SERIAL_BPS, SERIAL_8N1, MP3_RX, MP3_TX);
  if (!MP3Stream) {
    PRINTS("Invalid serial pin configuration, check config"); 
    while (1) {
      delay (1000);
    }
  } else {
    PRINTS("MP3 Player setup done.");
  } 

  PRINTS("\nBeginning MP3 player...");
  mp3.begin();
  PRINT("\nStatus code: ", mp3.getStsCode());
  mp3.wakeUp();
  
  mp3.setSynchronous(false);
  mp3.setCallback(cbResponse);
  
  vol = mp3.volumeMax();
  PRINT("\nSetting volume to max: ", vol);
  bool b = mp3.volume(vol);
  PRINT(" result ", b);
}

struct sound_info {
  uint8_t index;
  char *name;  
};

struct sound_collection {
  struct sound_info sounds[10];
  uint16_t max_index;
};

struct sound_collection sound_map;

char midnight[] = "midnight city";
char redlight[] = "red light";
char middleofnight[] = "middle of the night";
char bullettrain[] = "bullet train";
char collectcall[] = "collect call";
char rocketman[] = "rocket man";
char spaceoddity[] = "space oddity";

void init_sound(){
  sound_map.sounds[0].index = 64;
  sound_map.sounds[0].name = midnight;

  sound_map.sounds[1].index = 62;
  sound_map.sounds[1].name = redlight;

  sound_map.sounds[2].index = 61;
  sound_map.sounds[2].name = middleofnight;

  sound_map.sounds[3].index = 63;
  sound_map.sounds[3].name = bullettrain;

  sound_map.sounds[4].index = 62;
  sound_map.sounds[4].name = collectcall;

  sound_map.sounds[5].index = 65;
  sound_map.sounds[5].name = rocketman;

  sound_map.sounds[6].index = 66;
  sound_map.sounds[6].name = spaceoddity;  

  sound_map.max_index = 6;
}

struct sound_info* find_sound_info(char *name){
  uint16_t i = 0;
  struct sound_info* cur;
  Serial.println("Max index:");
  Serial.println(sound_map.max_index);
  while(i <= sound_map.max_index){
    if(strcmp(sound_map.sounds[i].name, name) == 0){
      cur = &sound_map.sounds[i];
      i = 999;
    }
    
    i = i+1;
  }
  return cur;
}

unsigned long start_time;
void setup() {
  start_time = millis();
  Serial.begin(115200);
  Serial.println("Initialize...");
  pixels.begin();
  pixelsExternal.begin();
  clear_sound_buffer();
  setup_mp3();
  init_sound();
  
  Serial2.begin(115200, SERIAL_8N1, VOICE_RX, VOICE_TX);
  setup_wifi();
  init_wot_config();
  setup_wot_td();
}

struct color_information {
  uint8_t index;
  uint8_t keep_previous;
  uint16_t time;
  uint8_t r;
  uint8_t g;
  uint8_t b;
};

struct color_state{
  uint16_t index;
  unsigned long previous_time;
  uint16_t current_repeat;
  uint16_t max_repeat;
  uint16_t max_index;
};

struct color_state base_color_state;
struct color_information *previous_base_color;
struct color_information base_color_buffer[BASE_COLOR_BUFFER_SIZE];
void clear_base_buffer(){
  previous_base_color->keep_previous = false;
  previous_base_color->index = 0;
  previous_base_color->r = 0;
  previous_base_color->g = 0;
  previous_base_color->b = 0;

  base_color_state.current_repeat = 0;
  base_color_state.index = 0;
  base_color_state.previous_time = 0;
  base_color_state.max_index = 0;
  base_color_state.max_repeat = 0;
  memset(base_color_buffer, 0, BASE_COLOR_BUFFER_SIZE);
}

struct color_state head_color_state;
struct color_information *previous_head_color;
struct color_information head_color_buffer[HEAD_COLOR_BUFFER_SIZE];
void clear_head_buffer(){
  previous_head_color->keep_previous = false;
  previous_head_color->index = 0;
  previous_head_color->r = 0;
  previous_head_color->g = 0;
  previous_head_color->b = 0;

  head_color_state.current_repeat = 0;
  head_color_state.index = 0;
  head_color_state.previous_time = 0;
  head_color_state.max_index = 0;
  head_color_state.max_repeat = 0;
  memset(head_color_buffer, 0, HEAD_COLOR_BUFFER_SIZE);
}


void clear_sound_buffer(){
  mp3_sound_state.current_repeat = 0;
  mp3_sound_state.max_repeat = 0;
  mp3_sound_state.index = 0;
  mp3_sound_state.max_index = 0;
  mp3_sound_state.last_chip_response = 0;
  mp3_sound_state.previous_time = 0;
  mp3_sound_state.last_successful = true;
  mp3_sound_state.stop = false;

  memset(sound_buffer, 0, SOUND_BUFFER_SIZE);
}

struct color_state moon_color_state;
struct color_information *previous_moon_color;
struct color_information moon_color_buffer[MOON_COLOR_BUFFER_SIZE];
void clear_moon_buffer(){
  previous_moon_color->keep_previous = false;
  previous_moon_color->index = 0;
  previous_moon_color->r = 0;
  previous_moon_color->g = 0;
  previous_moon_color->b = 0;

  moon_color_state.current_repeat = 0;
  moon_color_state.index = 0;
  moon_color_state.previous_time = 0;
  moon_color_state.max_index = 0;
  moon_color_state.max_repeat = 0;
  memset(moon_color_buffer, 0, MOON_COLOR_BUFFER_SIZE);
}

void setup_wot_td(){
  create_base_light_input();
  create_head_light_input();
  create_moon_light_input();
  create_sound_input();
  create_stop_sound_input();
  adapter->addDevice(&bitBlock);
  adapter->begin();
}

struct vc_cmd_information {
  uint8_t commands[10];
  uint16_t index;
  uint16_t max_index;
  uint16_t item_amount;
  unsigned long start_time;
};

uint16_t midnight_city = 0xB5;
uint16_t red_light = 0xB6;
uint16_t middle_of_night = 0xB7;
uint16_t bullet_train = 0xB8;
uint16_t collect_call = 0xB9;

struct vc_cmd_information vc_commands;

void clear_commands(){
  vc_commands.index = 0;
  vc_commands.max_index = 0;
  vc_commands.item_amount = 0;
  vc_commands.start_time = 0;
  memset(vc_commands.commands, 0, sizeof(vc_commands.commands));
}

void process_song(){
  if(vc_commands.item_amount >= 2){
    Serial.println("play");
    Serial.println(vc_commands.commands[1]);
    struct sound_info* to_play = NULL;
    switch(vc_commands.commands[1]){
      Serial.println("song:");
      Serial.println(vc_commands.commands[1]);
      case 0xB5:
        Serial.println("midnight city");
        to_play = find_sound_info("midnight city");
        break;
      case 0xB6:
        to_play = find_sound_info("red light");
        break;
      case 0xB7:
        Serial.println("middle of the night");
        to_play = find_sound_info("middle of the night");
        break;
      case 0xB8:
        to_play = find_sound_info("bullet train");
        break;
      case 0xB9:
        Serial.println("Collect call");
        to_play = find_sound_info("collect call");
        break;
      case 0xCC:
        Serial.println("rocket man");
        to_play = find_sound_info("rocket man");
        break;
      case 0xCD:
        Serial.println("space oddity");
        to_play = find_sound_info("space oddity");
        break;
      default:
        to_play = NULL;
    }
    if(to_play != NULL){
      clear_commands();
      clear_sound_buffer();
      sound_buffer[0] = {
        .index = to_play->index,
        .time = 99999
      };
      mp3_sound_state.max_index = 0;
      Serial.println("Play music:");
      Serial.println(to_play->index);
      mp3_sound_state.item_amount = 1;
    }else{
      Serial.println("Music is NULL");
    }
  }
}

void stop_music(){
  Serial.println("STOP SOUND");
  clear_sound_buffer();
  mp3_sound_state.stop = true;
}

void next_song(){

}

void prev_song(){

}

void play_from_start(){

}

void play_from_end(){
  
}

void affirmitive(){
  clear_commands();
  clear_sound_buffer();
  sound_buffer[0] = {
    .index = 26,
    .time = 10000
  };
  mp3_sound_state.max_index = 0;
  mp3_sound_state.item_amount = 1;
}

void process_commands(){
  if(vc_commands.item_amount > 0){
    Serial.println("Item amount:");
    Serial.println(vc_commands.item_amount);
    Serial.println(vc_commands.commands[0]);
    Serial.println(vc_commands.commands[1]);
    switch(vc_commands.commands[0]){
      case 0xA9:
        process_song();
        break;
      case 0xC3:
        stop_music();
        break;
      case 0xC8:
        next_song();
        break;
      case 0xC9:
        prev_song();
        break;
      case 0xCA:
        play_from_start();
        break;
      case 0xCB:
        play_from_end();
        break;
      case 0xCE:
        affirmitive();
        break;
    } 
  }
}

void speech_command_loop(unsigned long current_time){
  if(vc_commands.start_time > 0 && (vc_commands.start_time + 2000) <= current_time){
    clear_commands();
  }
  
  while(Serial2.available() > 0) {   
    uint8_t incoming = Serial2.read();

    if(incoming != 0xA0){
      Serial.println("I received: ");
      Serial.println(incoming, HEX);
      Serial.println("Index:");
      Serial.println(vc_commands.index);
      if(vc_commands.start_time == 0){
        vc_commands.start_time = current_time;
      }

      vc_commands.commands[vc_commands.index] = incoming;
      vc_commands.max_index = vc_commands.index + 1;
      vc_commands.index = vc_commands.index + 1;
      vc_commands.item_amount = vc_commands.index + 1;
    }
  }

  if(vc_commands.item_amount > 0){
    vc_commands.max_index = vc_commands.max_index - 1;
  }

  process_commands();
}


void base_light_loop(unsigned long current_time){
  if(base_color_state.index == 0){
    previous_base_color = &base_color_buffer[base_color_state.max_index];
  }else{
    previous_base_color = &base_color_buffer[base_color_state.index - 1];
  }

  if (
      (base_color_state.index == 0 && base_color_state.current_repeat == 0) || 
      (
        (current_time - base_color_state.previous_time) >= previous_base_color->time && 
        previous_base_color->time > 0 &&
        base_color_state.current_repeat < base_color_state.max_repeat
      )
   ) {
    if(base_color_state.index == base_color_state.max_index){
      base_color_state.current_repeat = base_color_state.current_repeat + 1;
    }
    struct color_information *base_color = &base_color_buffer[base_color_state.index];

    base_color_state.previous_time = current_time;

    if(!base_color->keep_previous){
      pixels.clear();
      pixels.show();
    }
    pixels.setPixelColor(base_color->index, pixels.Color(base_color->r, base_color->g, base_color->b));
    pixels.show();

    if(base_color_state.index == base_color_state.max_index){
      base_color_state.index = 0;
    }else{
      base_color_state.index = base_color_state.index + 1;
    }
  }
}

void head_light_loop(unsigned long current_time){
  if(head_color_state.index == 0){
    previous_head_color = &head_color_buffer[head_color_state.max_index];
  }else{
    previous_head_color = &head_color_buffer[head_color_state.index - 1];
  }

  if (
      (head_color_state.index == 0 && head_color_state.current_repeat == 0) || 
      (
        (current_time - head_color_state.previous_time) >= previous_head_color->time && 
        previous_head_color->time > 0 &&
        head_color_state.current_repeat < head_color_state.max_repeat
      )
   ) {
    if(head_color_state.index == head_color_state.max_index){
      head_color_state.current_repeat = head_color_state.current_repeat + 1;
    }
    struct color_information *base_color = &head_color_buffer[head_color_state.index];

    head_color_state.previous_time = current_time;

    pixelsExternal.clear();
    pixelsExternal.show();
    pixelsExternal.setPixelColor(4, pixelsExternal.Color(base_color->r, base_color->g, base_color->b));
    pixelsExternal.show();

    if(head_color_state.index == head_color_state.max_index){
      head_color_state.index = 0;
    }else{
      head_color_state.index = head_color_state.index + 1;
    }
  }
}


void moon_light_loop(unsigned long current_time){
  if(moon_color_state.index == 0){
    previous_moon_color = &moon_color_buffer[moon_color_state.max_index];
  }else{
    previous_moon_color = &moon_color_buffer[moon_color_state.index - 1];
  }

  if (
      (moon_color_state.index == 0 && moon_color_state.current_repeat == 0) || 
      (
        (current_time - moon_color_state.previous_time) >= previous_moon_color->time && 
        previous_moon_color->time > 0 &&
        moon_color_state.current_repeat < moon_color_state.max_repeat
      )
   ) {
    if(moon_color_state.index == moon_color_state.max_index){
      moon_color_state.current_repeat = moon_color_state.current_repeat + 1;
    }
    struct color_information *base_color = &moon_color_buffer[moon_color_state.index];

    moon_color_state.previous_time = current_time;

    pixelsExternal.clear();
    pixelsExternal.show();
    pixelsExternal.setPixelColor(1, pixelsExternal.Color(base_color->r, base_color->g, base_color->b));
    pixelsExternal.setPixelColor(2, pixelsExternal.Color(base_color->r, base_color->g, base_color->b));
    pixelsExternal.setPixelColor(3, pixelsExternal.Color(base_color->r, base_color->g, base_color->b));
    pixelsExternal.show();

    if(moon_color_state.index == moon_color_state.max_index){
      moon_color_state.index = 0;
    }else{
      moon_color_state.index = moon_color_state.index + 1;
    }
  }
}

//Fixme: Loop broken when request is only one item
void mp3_loop(unsigned long current_time){
  if(mp3_sound_state.stop && mp3_sound_state.last_chip_response != MD_YX5300::STS_ACK_OK){
    mp3.playStop();
  }else if(mp3_sound_state.stop && mp3_sound_state.last_chip_response == MD_YX5300::STS_ACK_OK){
    mp3_sound_state.stop = false;
  }

  if(mp3_sound_state.index == 0){
    previous_mp3_sound = &sound_buffer[mp3_sound_state.max_index];
  }else{
    previous_mp3_sound = &sound_buffer[mp3_sound_state.index - 1];
  }

  if(!mp3_sound_state.last_successful){
    mp3.playTrack(current_mp3_sound->index);
    if(mp3_sound_state.last_chip_response == MD_YX5300::STS_ACK_OK){
      mp3_sound_state.last_chip_response = 0;
      mp3_sound_state.last_successful = true;
      Serial.println("Changed track.");

      if(mp3_sound_state.index == mp3_sound_state.max_index){
        mp3_sound_state.index = 0;
      }else{
        mp3_sound_state.index = mp3_sound_state.index + 1;
      }
    }
  }


  if(      
      (mp3_sound_state.index == 0 && mp3_sound_state.current_repeat == 0 && mp3_sound_state.item_amount > 0 ) || 
      (
        mp3_sound_state.last_successful &&
        (current_time - mp3_sound_state.previous_time) >= previous_mp3_sound->time && 
        previous_mp3_sound->time > 0 &&
        mp3_sound_state.current_repeat < mp3_sound_state.max_repeat
      )
    ){
    Serial.println("Sound check loop");
    
    mp3_sound_state.last_successful = false;
    if(mp3_sound_state.index == mp3_sound_state.max_index){
      mp3_sound_state.current_repeat = mp3_sound_state.current_repeat + 1;
    }
    current_mp3_sound = &sound_buffer[mp3_sound_state.index];  

      
    mp3_sound_state.previous_time = current_time;
    mp3.playTrack(current_mp3_sound->index);

    if(mp3_sound_state.last_chip_response == MD_YX5300::STS_ACK_OK){
      mp3_sound_state.last_chip_response = 0;
      mp3_sound_state.last_successful = true;
      Serial.println("Changed track.");

      if(mp3_sound_state.index == mp3_sound_state.max_index){
        mp3_sound_state.index = 0;
      }else{
        mp3_sound_state.index = mp3_sound_state.index + 1;
      }

    }else{
      mp3_sound_state.last_successful = false;
    }
    
  }
}

unsigned long last_time = 0;
bool is_lit = false;
void loop() {
  unsigned long current_time = millis();
  speech_command_loop(current_time);
  base_light_loop(current_time);
  head_light_loop(current_time);
  moon_light_loop(current_time);
  mp3_loop(current_time);
  adapter->update();
  mp3.check();
}

void do_light_base(const JsonVariant &input){
  clear_base_buffer();
  JsonObject inputObj = input.as<JsonObject>();
  
  JsonArray itemArray = inputObj["data"].as<JsonArray>();
  base_color_state.max_repeat = inputObj["repeat"].as<unsigned int>();
  Serial.println(base_color_state.max_repeat);
  

  int i = 0;
  for (JsonArray value : itemArray) {
    
    if(i < BASE_COLOR_BUFFER_SIZE - 1){
      base_color_buffer[i] = {
        .index = value[1],
        .keep_previous = value[0],
        .time = value[2],
        .r = value[3],
        .g = value[4],
        .b = value[5]
      };
      Serial.println(base_color_buffer[i].index);
      base_color_state.max_index = i;

      i++;
    }
  }
}


void do_light_head(const JsonVariant &input){
  Serial.println("LIGHT UP HEAD");
  clear_head_buffer();
  JsonObject inputObj = input.as<JsonObject>();
  
  JsonArray itemArray = inputObj["data"].as<JsonArray>();
  head_color_state.max_repeat = inputObj["repeat"].as<unsigned int>();

  int i = 0;
  for (JsonArray value : itemArray) {
    
    if(i < HEAD_COLOR_BUFFER_SIZE - 1){
      head_color_buffer[i] = {
        .time = value[0],
        .r = value[1],
        .g = value[2],
        .b = value[3]
      };
      head_color_state.max_index = i;

      i++;
    }
  }
}

void do_light_moon(const JsonVariant &input){
  Serial.println("LIGHT UP MOON");
  clear_moon_buffer();
  JsonObject inputObj = input.as<JsonObject>();
  
  JsonArray itemArray = inputObj["data"].as<JsonArray>();
  moon_color_state.max_repeat = inputObj["repeat"].as<unsigned int>();

  int i = 0;
  for (JsonArray value : itemArray) {
    
    if(i < HEAD_COLOR_BUFFER_SIZE - 1){
      moon_color_buffer[i] = {
        .time = value[0],
        .r = value[1],
        .g = value[2],
        .b = value[3]
      };
      moon_color_state.max_index = i;

      i++;
    }
  }
}

void do_sound(const JsonVariant &input){
  clear_sound_buffer();
  Serial.println("SOUND");
  JsonObject inputObj = input.as<JsonObject>();

  JsonArray itemArray = inputObj["data"].as<JsonArray>();
  mp3_sound_state.max_repeat = inputObj["repeat"].as<unsigned int>();

  int i = 0;
  for (JsonArray value : itemArray) {
    
    if(i < SOUND_BUFFER_SIZE - 1){
      Serial.println("SOUND LOOP");
      Serial.println();
      sound_buffer[i] = {
        .index = value[0],
        .time = value[1]
      };
      mp3_sound_state.max_index = i;
      Serial.println(sound_buffer[i].index);
      Serial.println(sound_buffer[i].time);
      mp3_sound_state.item_amount = mp3_sound_state.item_amount + 1;
      i++;
    }
  }
  Serial.println("SOUND LOOP DONE");
  mp3_sound_state.max_index = mp3_sound_state.max_index -1;
  Serial.println(mp3_sound_state.max_index);
}

void do_stop_sound(const JsonVariant &input){
  Serial.println("STOP SOUND");
  clear_sound_buffer();
  mp3_sound_state.stop = true;
}

ThingActionObject *base_light_action_generator(DynamicJsonDocument *input) {
  return new ThingActionObject("baseLightAction", input, do_light_base, nullptr);
}

ThingActionObject *moon_light_action_generator(DynamicJsonDocument *input) {
  return new ThingActionObject("moonLightAction", input, do_light_moon, nullptr);
}

ThingActionObject *head_light_action_generator(DynamicJsonDocument *input) {
  return new ThingActionObject("headLightAction", input, do_light_head, nullptr);
}

ThingActionObject *sound_action_generator(DynamicJsonDocument *input) {
  return new ThingActionObject("soundLightAction", input, do_sound, nullptr);
}

ThingActionObject *stop_sound_action_generator(DynamicJsonDocument *input) {
  return new ThingActionObject("stopSoundAction", input, do_stop_sound, nullptr);
}

