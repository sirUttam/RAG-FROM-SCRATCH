def chunk_text(text: str, chunk_size: int, overlap: int):
    chunks = []
    start = 0
    
    while start < len(text):
        
        end = start+chunk_size
        
        chunk = text[start:end]      
        chunks.append(chunk)
        
        if len(text) <= end:    # This makes sure, we stop when the final chunk reaches the end of the text.
            break
        
        start = end - overlap    #Overlap: It repeats some text across neighboring chunks, reducing the chance of losing context.
        
    return chunks
        
        