#include <FastLED.h>

#define NUM_LEDS 14          // Number of LEDs on the strip
#define DATA_PIN 3           // Data pin for the strip

#define CMD_BUFFER_SIZE 32   // Size of the command buffer
#define SERIAL_BAUD 115200   // Baud rate for serial communication
#define CMD_START '['        // Start character of a command
#define CMD_END ']'          // End character of a command

char cmdBuffer[CMD_BUFFER_SIZE]; // Circular buffer for command strings
volatile byte cmdHead = 0;        // Index to insert new command
volatile byte cmdTail = 0;        // Index to read oldest command
volatile bool newData = false;    // Indicates if there's new data

CRGB leds[NUM_LEDS];

void setup()
{
    FastLED.addLeds<WS2812B, DATA_PIN, GRB>(leds, NUM_LEDS);
    Serial.begin(SERIAL_BAUD);
    Serial.println("Ready for commands");
}

void loop()
{
    receiveData();
    if (newData)
    {
        processCommands();
        newData = false;
    }
}

// Receives command data from Serial
void receiveData()
{
    while (Serial.available() > 0)
    {
        char rc = Serial.read();
        if (rc == CMD_START)
        {
            cmdBuffer[cmdHead++] = '\0'; // Null-terminate the command string
            newData = true;              // Set the flag to indicate new data
            if (cmdHead >= CMD_BUFFER_SIZE)
            {
                cmdHead = 0; // Wrap around if the buffer is full
            }
        }
        else
        {
            cmdBuffer[cmdHead++] = rc; // Store the received character in the buffer
            if (cmdHead >= CMD_BUFFER_SIZE)
            {
                cmdHead = 0; // Wrap around if the buffer is full
            }
        }
    }
}

// Processes all available commands
void processCommands()
{
    while (cmdTail != cmdHead)
    {
        // Read command from buffer
        char cmd[CMD_BUFFER_SIZE];
        byte i = 0;
        while (cmdTail != cmdHead && cmdBuffer[cmdTail] != '\0')
        {
            cmd[i++] = cmdBuffer[cmdTail++];
            if (cmdTail >= CMD_BUFFER_SIZE)
            {
                cmdTail = 0; // Wrap around if the buffer is full
            }
        }
        cmd[i] = '\0'; // Null-terminate the command string
        if (cmdTail != cmdHead)
        {
            cmdTail++; // Move to next command if available
            if (cmdTail >= CMD_BUFFER_SIZE)
            {
                cmdTail = 0; // Wrap around if the buffer is full
            }
        }

        // Process command
        char *cmdName = strtok(cmd, ",");
        if (strcmp(cmdName, "RGB") == 0)
        {
            setRgb();
        }
        else if (strcmp(cmdName, "I") == 0)
        {
            Individual();
        }
        // Add more commands as needed
    }
}

// Sets the RGB values for the LEDs
void setRgb()
{
    byte r = atoi(strtok(NULL, ","));
    byte g = atoi(strtok(NULL, ","));
    byte b = atoi(strtok(NULL, ","));
    
    fill_solid(leds, NUM_LEDS, CRGB(r, g, b));
    FastLED.show();
}

// Sets the Individual RGB values for the LEDs
void Individual()
{
  byte r = atoi(strtok(NULL, ","));
  byte g = atoi(strtok(NULL, ","));
  byte b = atoi(strtok(NULL, ","));
  byte i = atoi(strtok(NULL, "," ));
  byte e = atoi(strtok(NULL, ","));
  if (e == 1);
  {
    fill_solid(leds, NUM_LEDS, CRGB(0,0,0));
  }
  leds[i] = CRGB(r,g,b);
  FastLED.show();
}
