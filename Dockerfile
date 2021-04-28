FROM heinzdf/oubnew:latest
 
# Clone repo and prepare working directory
RUN git clone -b main https://github.com/rizgustiadi/AkenoXNew /OUBnew
RUN chmod 777 /OUBnew
WORKDIR /OUBnew
 
# Install requirements
CMD ["python3","-m","userbot"]
