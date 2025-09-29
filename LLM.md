# Eve

I used Google and the AI Overview (Gemini?) gave me a response which I used. I searched "if integer is byte python how to make byte type", because I was trying to get `decrypt.decode("utf-16")` to work, but `decrypt` (a value in the list of decrypted bytes) was an integer and not a byte. I'm not as familiar with Python syntax and I have found that I cannot predict how it does type conversion with bytes, so I was googling to find the syntax. I got the following response:

> To create a bytes object from an integer in Python, particularly if that integer represents a single byte value (0-255), there are a few methods.
> 
> 1. Using int.to_bytes():
> This method is suitable for converting any integer into a sequence of bytes. You need to specify the desired length of the byte sequence and the byte order.
>
> ```
> integer_value = 100
> # Convert to a single byte (length=1) in big-endian order
> byte_object = integer_value.to_bytes(1, byteorder='big')
> print(f"Integer {integer_value} converted to bytes: {byte_object}")
> ```
> ...

When I tried `integer_value.to_bytes(1, byteorder='big')` on on my decrypted values, I got the error that `int too big to convert`. The AI code had the comment of `Convert to a single byte (length=1)` which made me wonder if I was dealing with a single or more bytes, so then I tried `integer_value.to_bytes(2, byteorder='big')` which was successful. 