#include <ESP8266WiFi.h>

// Network information.
//#define WIFI_NAME "Alfred jio"
//#define PASSWORD "ruban1120"
const char* ssid = "Alfred jio";
const char* password = "ruban1120";

// Hardware information.
#define SENSOR_POWER 13                            // Connect the power for the soil sensor here.
#define SOIL_PIN A0                                // Connect the sensor output pin here.
#define TIMEOUT  5000                              // Timeout for server response.
#define SLEEP_TIME_SECONDS 60

// ThingSpeak information.
#define NUM_FIELDS 2                               // To update more fields, increase this number and add a field label below.
#define SOIL_MOISTURE_FIELD 1                      // ThingSpeak field for soil moisture measurement.
#define ELAPSED_TIME_FIELD 2                       // ThingSpeak field for elapsed time from startup.
#define THING_SPEAK_ADDRESS "api.thingspeak.com"
String writeAPIKey="S54UHKWRXCPL2BJV";             // Change this to the write API key for your channel.

// Global variables. 
int numMeasure = 5;                                // Number of measurements to average.
int ADCValue = 0;                                  // Moisture sensor reading.
                         
WiFiClient client;

// Put your setup code here, to run once:
void setup()
{
  Serial.begin(115200);
  delay(10);
  Serial.println("Connecting to ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);
  while (WiFi.status()!=WL_CONNECTED)
  {
    delay(500);
    Serial.print(".");
    
  }
  Serial.println("");
  Serial.println("WiFi connected");
  pinMode( SENSOR_POWER , OUTPUT );
  digitalWrite( SENSOR_POWER , LOW );   // Set to LOW so no power is flowing through the sensor.
}

// Put your main code here, to run repeatedly:
void loop()
{
    // Write to successive fields in your channel by filling fieldData with up to 8 values.
    String fieldData[ NUM_FIELDS ];  

    // You can write to multiple fields by storing data in the fieldData[] array, and changing numFields.        
    // Write the moisture data to field 1.
    fieldData[ SOIL_MOISTURE_FIELD ] = String( readSoil( numMeasure ) ); 
    Serial.print( "Soil Moisture = " );
    Serial.println( fieldData[ SOIL_MOISTURE_FIELD ] );
    
    // Write the elapsed time from startup to Field 2.
    fieldData[ ELAPSED_TIME_FIELD ] = String( millis() ); 
    
    HTTPPost( NUM_FIELDS , fieldData );
    
    delay( 1000 );
    Serial.print( "Goodnight for "+String( SLEEP_TIME_SECONDS ) + " Seconds" );
    ESP.deepSleep( SLEEP_TIME_SECONDS * 1000000 );
    // If you disable sleep mode, add delay so you don't post to ThingSpeak too often.
    // delay( 20000 );
}

// This function reads the soil moisture sensor numAve times and returns the average.
long readSoil(int numAve)
{
  long ADCValue = 0;
  
  for ( int i = 0; i < numAve; i++ ) {
    digitalWrite( SENSOR_POWER, HIGH );  // Turn power to device on.
    delay(10);    // Wait 10 milliseconds for sensor to settle.
    ADCValue += analogRead( SOIL_PIN );     // Read the value from sensor.
    digitalWrite( SENSOR_POWER, LOW );   // Turn power to device off.
  }
  
  ADCValue = ADCValue / numAve;
  return ADCValue;                    // Return the moisture value.
}

// Connect to the local Wi-Fi network
//int connectWifi()
//{
    
 //   while (WiFi.status() != WL_CONNECTED) 
//    {
//        WiFi.begin( WIFI_NAME , PASSWORD );
   //     Serial.println( "Connecting to Wi-Fi" );
  //      delay( 200 );
 //   }
//    Serial.println( "Connected" );  // Inform the serial monitor.
//}

// This function builds the data string for posting to ThingSpeak
    // and provides the correct format for the wifi client to communicate with ThingSpeak.
    // It posts numFields worth of data entries, and takes the
    // data from the fieldData parameter passed to it. 
  
int HTTPPost( int numFields , String fieldData[] ){
  
    if (client.connect( THING_SPEAK_ADDRESS , 80 )){

       // Build the postData string.  
       // If you have multiple fields, make sure the sting does not exceed 1440 characters.
       String postData= "api_key=" + writeAPIKey ;
       for ( int fieldNumber = 1; fieldNumber < numFields+1; fieldNumber++ ){
            String fieldName = "field" + String( fieldNumber );
            postData += "&" + fieldName + "=" + fieldData[ fieldNumber ];
            
            }

        // POST data via HTTP.
        Serial.println( "Connecting to ThingSpeak for update..." );
        Serial.println();
        
        client.println( "POST /update HTTP/1.1" );
        client.println( "Host: api.thingspeak.com" );
        client.println( "Connection: close" );
        client.println( "Content-Type: application/x-www-form-urlencoded" );
        client.println( "Content-Length: " + String( postData.length() ) );
        client.println();
        client.println( postData );
        
        Serial.println( postData );
        
        String answer=getResponse();
        Serial.println( answer );
    }
    else
    {
      Serial.println ( "Connection Failed" );
    }
    
}

// Wait for a response from the server indicating availability,
// and then collect the response and build it into a string.

String getResponse(){
  String response;
  long startTime = millis();

  delay( 200 );
  while ( client.available() < 1 && (( millis() - startTime ) < TIMEOUT ) ){
        delay( 5 );
  }
  
  if( client.available() > 0 ){ // Get response from server.
     char charIn;
     do {
         charIn = client.read(); // Read a char from the buffer.
         response += charIn;     // Append the char to the string response.
        } while ( client.available() > 0 );
    }
  client.stop();
        
  return response;
}
