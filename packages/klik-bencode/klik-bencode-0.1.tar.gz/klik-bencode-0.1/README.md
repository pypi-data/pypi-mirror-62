Bencoder Decoder Library 
------------------------
A python library to decode the Bencode String to native Python data types i.e int,str,list and dictionary.

**How to use:**
There are two ways to use this Library.

a) *Clone GitHub Repo*: 
 * Clone the github repo `https://github.com/malhotraguy/klik_interview`
 
```
  from bencode.bencode_decoder import decoder
  bencode_data = "8:robots54"
  decoded_value = decoder(bencode_data=bencode_data)
  print(decoded_value)
  # robots54
  bencode_data = "l5:green3:red4:bluee"
  decoded_value = decoder(bencode_data=bencode_data)
  print(decoded_value)
  # ["green", "red", "blue"]
   ```
 * For more examples refer to tests folder.

b) *Install as python library*:
 * Install the library: `pip install klik-bencode==0.1`
 ```
  from bencode.bencode_decoder import decoder
  bencode_data = "8:robots54"
  decoded_value = decoder(bencode_data=bencode_data)
  print(decoded_value)
  # robots54
  bencode_data = "l5:green3:red4:bluee"
  decoded_value = decoder(bencode_data=bencode_data)
  print(decoded_value)
  # ["green", "red", "blue"]
   ```