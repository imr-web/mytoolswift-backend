from fastapi import FastAPI, File, UploadFile
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware
from rembg import remove, new_session
import io
from PIL import Image

app = FastAPI()

# This tells the server who is allowed to use the AI
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://mytoolswift.com",
        "https://www.mytoolswift.com",
        "https://cv.mytoolswift.com"
    ],
    allow_credentials=True,
    allow_methods=["POST"],
    allow_headers=["*"],
)

# We use 'u2netp' because it's the high-speed "Pocket" version for mobile/low-RAM
session = new_session("u2netp")

@app.get("/")
def status_check():
    return {"message": "MyToolSwift Engine is Online"}

@app.post("/api/remove-bg")
async def remove_background(image_file: UploadFile = File(...)):
    try:
        # Read the user's image
        contents = await image_file.read()
        input_image = Image.open(io.BytesIO(contents))
        
        # The AI Magic happens here
        output_image = remove(input_image, session=session)
        
        # Convert the result to a PNG
        img_byte_arr = io.BytesIO()
        output_image.save(img_byte_arr, format='PNG')
        
        return Response(content=img_byte_arr.getvalue(), media_type="image/png")
    except Exception as e:
        return {"error": str(e)}
