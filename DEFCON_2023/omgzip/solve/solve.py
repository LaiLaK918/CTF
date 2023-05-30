from omgzip import compress,decompress

def decom(filename):
    with open(filename, "rb") as input_file:
        input_data = input_file.read()
    output_data = decompress(input_data)
    return output_data


f = open('flag.txt','wb')
f.write(decom('data.tar.omgzip'))
f.close()
