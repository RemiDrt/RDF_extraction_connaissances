#!/usr/bin/python
#coding=utf-8
print("Hello world")
#opening the file in read only
NRI_File = open("../Graphes_attribués_NRI/acl_XP1_aut_pub.nri", encoding="utf-8")
print("my file is open")
#reading the file
content = NRI_File.read()
print(content)


#don't forget to close the file
NRI_File.close()
