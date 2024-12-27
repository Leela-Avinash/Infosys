from MileStone_1.speech_to_text import record_audio, transcribe_audio
from MileStone_1.generate_response import generate_response
from MileStone_1.text_to_speech import text_to_speech
from MileStone_2.Analyze_text import analyze_audio
import time

def main():
    print("\n🛒 **Welcome to the Real-Time AI Sales Assistant!** 🛒")
    print("Say 'exit' to end the chat.\n")

    while True:
        print("You: ")
        print("Listening for your input...")
        start = time.time()
        audio_file = record_audio()
        print(audio_file)
        transcribed_text = transcribe_audio(audio_file)
        print(f"Transcribed Text: {transcribed_text}")

        if "exit" in transcribed_text.lower():
            transcribed_text = "Goodbye! Have a great day! 👋"
            print(transcribed_text)
            text_to_speech(transcribed_text)
            break
        
        summary = analyze_audio(transcribed_text)
        ai_response = generate_response(transcribed_text, summary)
        print("\nAI Sales Assistant:", ai_response, "\n")
        print(f"Time taken: {time.time() - start:.2f} seconds")

        text_to_speech(ai_response)

if __name__ == "__main__":
    main()
