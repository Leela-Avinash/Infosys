import csv
from MileStone_1.speech_to_text import record_audio, transcribe_audio
from MileStone_1.generate_response import generate_response
from MileStone_1.text_to_speech import text_to_speech
from MileStone_2.Analyze_user_audio import analyze_audio
from MileStone_2.Analyze_user_statement import Analyze_text
from MileStone_3.Reccomendations import recommend
from MileStone_3.PostCallAnalysis import generate_summary
import time
import datetime

def read_csv_content(csv_file):
    conversation = []
    with open(csv_file, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader, None) 
        for row in reader:
            if len(row) == 2: 
                conversation.append(f"User: {row[0]} AI: {row[1]}")
    return " ".join(conversation)

def get_next_interaction_id(csv_file):
    with open(csv_file, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader, None)  # Skip header
        interaction_ids = [int(row[0]) for row in reader]
        return max(interaction_ids, default=0) + 1

def main():
    print("\n🛒 **Welcome to the Real-Time AI Sales Assistant!** 🛒")
    print("Say 'exit' to end the chat.\n")
    customer_id = 1

    csv_file = "conversation_log.csv"
    interaction_csv_file = "D:/Codes/Deep_Learning/Infosys_internship/Real-Time-AI-Sales-Intelligence-and-Sentiment-Driven-Deal-Negotiation-Assistant/Assignments/MileStone_3/mnt/data/interactions.csv"

    # Open files once at the start and keep them open during the conversation
    with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, quotechar='"', quoting=csv.QUOTE_ALL)
        writer.writerow(["User", "Interaction"])  

    with open(csv_file, mode='a', newline='', encoding='utf-8') as file, \
         open(interaction_csv_file, mode='a', newline='', encoding='utf-8') as interaction_file:

        writer = csv.writer(file, quotechar='"', quoting=csv.QUOTE_ALL)
        interaction_writer = csv.writer(interaction_file, quotechar='"', quoting=csv.QUOTE_ALL)

        while True:
            print("You: ")
            print("Listening for your input...")
            # audio_file = record_audio()
            start = time.time()
            audio_file = "temp_recording.wav"
            print(audio_file)
            
            transcription_start = time.time()
            transcribed_text = transcribe_audio(audio_file)
            writer.writerow(["User", transcribed_text])
            print(f"Transcribed Text: {transcribed_text}")
            print("Time taken for transcription:", time.time() - transcription_start)

            if "exit" in transcribed_text.lower():
                ai_response = "Goodbye! Have a great day!"
                print(ai_response)
                text_to_speech(ai_response)
                full_conversation = read_csv_content(csv_file)
                analysis = Analyze_text(full_conversation)
                post_call_analysis = generate_summary(full_conversation, analysis)
                print("Post Call Analysis")
                print(post_call_analysis)
                break

            summary_start = time.time()
            summary = analyze_audio(audio_file)
            print(summary["sentiment"], summary["tone"], summary["intent"])
            print(summary)

            interaction_id = get_next_interaction_id(interaction_csv_file)
            interaction_writer.writerow([int(interaction_id), int(customer_id), datetime.datetime.now(), "call", transcribed_text, summary["sentiment"], summary["tone"], summary["intent"]])
            print(f"Time taken for summary: {time.time() - summary_start:.2f} seconds")
            
            recommended_terms = recommend(1, transcribed_text, sentiment=summary["sentiment"], intent=summary["intent"], tone=summary["tone"])
            response_start = time.time()
            ai_response = generate_response(transcribed_text, recommended_terms=recommended_terms, sentiment=summary["sentiment"], intent=summary["intent"], tone=summary["tone"])
            writer.writerow(["AI Response", ai_response])
            print("\nAI Sales Assistant:", ai_response, "\n")
            print(f"Time taken for response generation: {time.time() - response_start:.2f} seconds")
            print(f"Total Time taken: {time.time() - start:.2f} seconds")
            
            text_to_speech(ai_response)

if __name__ == "__main__":
    main()