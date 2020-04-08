const int REED_PIN = 2; // Pin connected to reed switch
const int LED_PIN = 13; // LED pin - active-high

const char string_0[] PROGMEM = "A=3.601  B=4.538  C=3.343  D=3.237  E=0.000 F=0.000";
const char string_1[] PROGMEM = "A=9.999  B=9.999  C=4.149  D=4.657  E=0.000 F=0.000";
const char string_2[] PROGMEM = "A=3.219  B=3.195  C=3.23  D=3.193  E=0.000 F=0.000";
const char string_3[] PROGMEM = "A=3.415  B=3.359  C=3.165  D=3.311  E=0.000 F=0.000";
const char string_4[] PROGMEM = "A=3.231  B=3.257  C=3.407  D=3.414  E=0.000 F=0.000";
const char string_5[] PROGMEM = "A=3.673  B=3.691  C=3.439  D=3.245  E=0.000 F=0.000";
const char string_6[] PROGMEM = "A=3.285  B=9.999  C=3.418  D=3.478  E=0.000 F=0.000";
const char string_7[] PROGMEM = "A=4.592  B=3.524  C=3.16  D=3.268  E=0.000 F=0.000";
const char string_8[] PROGMEM = "A=3.156  B=3.536  C=3.358  D=3.483  E=0.000 F=0.000";
const char string_9[] PROGMEM = "A=3.724  B=3.369  C=3.883  D=3.415  E=0.000 F=0.000";
const char string_10[] PROGMEM = "A=9.999  B=3.566  C=3.267  D=3.267  E=0.000 F=0.000";
const char string_11[] PROGMEM = "A=9.999  B=3.522  C=3.429  D=3.27  E=0.000 F=0.000";
const char string_12[] PROGMEM = "A=9.999  B=4.371  C=3.174  D=3.19  E=0.000 F=0.000";
const char string_13[] PROGMEM = "A=4.155  B=3.728  C=3.278  D=3.703  E=0.000 F=0.000";
const char string_14[] PROGMEM = "A=3.386  B=4.606  C=3.376  D=3.314  E=0.000 F=0.000";
const char string_15[] PROGMEM = "A=3.498  B=3.468  C=3.177  D=3.386  E=0.000 F=0.000";
const char string_16[] PROGMEM = "A=3.232  B=3.221  C=3.429  D=3.357  E=0.000 F=0.000";
const char string_17[] PROGMEM = "A=3.288  B=3.762  C=3.575  D=3.868  E=0.000 F=0.000";
const char string_18[] PROGMEM = "A=3.223  B=9.999  C=3.395  D=3.144  E=0.000 F=0.000";
const char string_19[] PROGMEM = "A=3.547  B=3.308  C=3.532  D=3.381  E=0.000 F=0.000";
const char string_20[] PROGMEM = "A=4.026  B=3.83  C=5.003  D=3.527  E=0.000 F=0.000";
const char string_21[] PROGMEM = "A=3.219  B=3.178  C=3.195  D=3.556  E=0.000 F=0.000";
const char string_22[] PROGMEM = "A=3.247  B=3.386  C=3.26  D=3.283  E=0.000 F=0.000";
const char string_23[] PROGMEM = "A=3.359  B=3.413  C=3.687  D=3.409  E=0.000 F=0.000";
const char string_24[] PROGMEM = "A=3.196  B=3.398  C=3.522  D=3.228  E=0.000 F=0.000";
const char string_25[] PROGMEM = "A=3.485  B=3.139  C=9.999  D=3.714  E=0.000 F=0.000";
const char string_26[] PROGMEM = "A=3.415  B=3.24  C=3.404  D=3.446  E=0.000 F=0.000";
const char string_27[] PROGMEM = "A=3.485  B=3.677  C=4.291  D=4.272  E=0.000 F=0.000";
const char string_28[] PROGMEM = "A=3.406  B=3.179  C=9.999  D=3.483  E=0.000 F=0.000";
const char string_29[] PROGMEM = "A=3.269  B=3.233  C=9.999  D=4.556  E=0.000 F=0.000";
const char string_30[] PROGMEM = "A=3.304  B=3.517  C=3.935  D=3.49  E=0.000 F=0.000";
const char string_31[] PROGMEM = "A=3.143  B=3.423  C=3.502  D=9.999  E=0.000 F=0.000";
const char string_32[] PROGMEM = "A=4.483  B=3.434  C=3.581  D=3.493  E=0.000 F=0.000";
const char string_33[] PROGMEM = "A=3.502  B=3.286  C=3.242  D=3.165  E=0.000 F=0.000";
const char string_34[] PROGMEM = "A=3.201  B=3.332  C=3.457  D=3.33  E=0.000 F=0.000";
const char string_35[] PROGMEM = "A=3.371  B=3.273  C=3.179  D=3.314  E=0.000 F=0.000";
const char string_36[] PROGMEM = "A=4.163  B=3.2  C=3.25  D=9.999  E=0.000 F=0.000";
const char string_37[] PROGMEM = "A=3.376  B=3.343  C=3.281  D=9.999  E=0.000 F=0.000";
const char string_38[] PROGMEM = "A=3.547  B=3.27  C=3.861  D=3.369  E=0.000 F=0.000";
const char string_39[] PROGMEM = "A=3.839  B=3.368  C=3.238  D=3.515  E=0.000 F=0.000";
const char *const string_table[] PROGMEM = {string_0, string_1, string_2, string_3, string_4, string_5, string_6, string_7, string_8, string_9, string_10, string_11, string_12, string_13, string_14, string_15, string_16, string_17, string_18, string_19, string_20, string_21, string_22, string_23, string_24, string_25, string_26, string_27, string_28, string_29, string_30, string_31, string_32, string_33, string_34, string_35, string_36, string_37, string_38, string_39, };


void setup() 
{
  Serial.begin(9600);
  Serial.println("ready");
}


int i = 0;
char buffer[128];

void loop() 
{


  for(;i < 40; i++)
  {
    strcpy_P(buffer, (char *)pgm_read_word(&(string_table[i]))); 
    Serial.println(buffer);
    delay(9000);
     Serial.println("@");
    delay(2000);
  }

  
 
  
}
