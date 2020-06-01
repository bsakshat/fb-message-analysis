# Facebook Message Parser
A simple program to parse and analyse facebook messages from downloaded file.

To run the program, download the fbmsg.py file from this repository.   
Put it in the same folder where you have downloaded the message files from facebook.  
Double click on the fbmsg.py file.  
When prompted for location of the message files, provide the relative path of the folder containing the message files.  
  
For example, in the following directory structure:  
<pre>
+-- fb-msg  
|   +-- messages
|       +-- group_A  
|           +-- message_file.json  
|   +-- fbmsg.py    

</pre>

If you want to process the message files inside group_A folder, provide 'messages\group_A' for windows or 'messages/group_A' for Linux (without the single quotes).    

A file will also be created named group_name_analysis.txt in the same folder as the fbmsg.py file.    

Updated from: https://gist.github.com/bsakshat/65c496ed73fc670d73eec95b9617a066  
The gist is cloned from: https://gist.github.com/multun/f487fc648de893c136298a8491ad5f16

