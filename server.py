import face_recognition
import asyncio
import websockets
import json, io

face = face_recognition.load_image_file("caminho/image.jpeg")
face_enconding = face_recognition.face_encodings(face)[0]

async def websocket_handler(websocket, path):
    try:
        async for message in websocket:
            response = recognize_face(message)
            await websocket.send(json.dumps(response))
    except Exception as err:
        print('WebSocket Error: '+str(err))


def recognize_face(message):
    try:
        unknown_picture = face_recognition.load_image_file(io.BytesIO(message))
        unknown_face_encodings = face_recognition.face_encodings(unknown_picture)
        if len(unknown_face_encodings) > 0:
            unknown_face_encoding = unknown_face_encodings[0]
        else:
            return {"status": True, "message": "No Face Detected", "data": 0}
        results = face_recognition.compare_faces([face_enconding], unknown_face_encoding)
        if results[0] == True:
            return {"status": True, "message": "Recognition successful", "data": 2}
        else:
            return {"status": True, "message": "Recognition unsuccessful", "data": 1}

    except Exception as err:
        return {"status": False, "message": str(err)}


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        websockets.serve(websocket_handler, "0.0.0.0", 8765)
    )
    loop.run_forever()
