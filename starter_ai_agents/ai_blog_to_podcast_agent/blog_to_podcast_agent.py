import os
from uuid import uuid4
from agno.agent import Agent, RunResponse
from agno.models.google import Gemini
from agno.tools.eleven_labs import ElevenLabsTools
from agno.tools.firecrawl import FirecrawlTools
from agno.utils.audio import write_audio_to_file
from agno.utils.log import logger
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

# Streamlit Page Setup
st.set_page_config(page_title="📰 ➡️ 🎙️ Blog to Podcast Agent", page_icon="🎙️")
st.title("📰 ➡️ 🎙️ Blog to Podcast Agent")


gemini_api_key = os.getenv("GEMINI_API_KEY")
elevenlabs_api_key = os.getenv("ELEVEN_LABS_API_KEY")
firecrawl_api_key = os.getenv("FIRECRAWL_API_KEY")

# Check if all keys are provided
keys_provided = all([gemini_api_key, elevenlabs_api_key, firecrawl_api_key])

# Voice Options - Updated with better Vietnamese voices
VOICE_OPTIONS = {
    # Vietnamese Voices (better quality)
    "Nguyễn Ngân (Female, Vietnamese)": "DvG3I1kDzdBY3u4EzYh6",         
    "Nhật Phong (Male, Vietnamese)": "RxhjHDfpO54FYotYtKpw",      # Using high-quality voice

    # Popular International Voices
    "Rachel (Female, American)": "21m00Tcm4TlvDq8ikWAM",
    "Drew (Male, American)": "29vD33N1CtxCmqQRPOHJ",

}

# Input: Blog URL
url = st.text_input("Enter the Blog URL:", "")

# Voice Selection
selected_voice = st.selectbox(
    "🎤 Choose Voice:",
    options=list(VOICE_OPTIONS.keys()),
    index=list(VOICE_OPTIONS.keys()).index("Nguyễn Ngân (Female, Vietnamese)"),  # Default to Vietnamese
    help="Select the voice for your podcast"
)

# Button: Generate Podcast
generate_button = st.button("🎙️ Generate Podcast", disabled=not keys_provided)

if not keys_provided:
    st.warning("Please provide all required API keys to enable podcast generation.")

if generate_button:
    if url.strip() == "":
        st.warning("Please enter a blog URL first.")
    else:
        # Set API keys as environment variables for Agno and Tools
        os.environ["GEMINI_API_KEY"] = gemini_api_key
        os.environ["ELEVEN_LABS_API_KEY"] = elevenlabs_api_key
        os.environ["FIRECRAWL_API_KEY"] = firecrawl_api_key

        with st.spinner("Processing... Scraping blog, summarizing and generating podcast 🎶"):
            try:
                blog_to_podcast_agent = Agent(
                    name="Blog to Podcast Agent",
                    agent_id="blog_to_podcast_agent",
                    model=Gemini(id="gemini-2.0-flash-exp", api_key=gemini_api_key),
                    tools=[
                        ElevenLabsTools(
                            voice_id=VOICE_OPTIONS[selected_voice],
                            model_id="eleven_turbo_v2_5",
                            target_directory="audio_generations",
                            api_key=elevenlabs_api_key,
                        ),
                        FirecrawlTools(api_key=firecrawl_api_key),
                    ],
                    description="You are an AI agent that can generate audio using the ElevenLabs API.",
                    instructions=[
                        "When the user provides a blog URL:",
                        "1. Use FirecrawlTools to scrape the blog content",
                        "2. Create a concise summary of the blog content that is NO MORE than 3000 characters long",
                        "3. The summary should capture the main points while being engaging and conversational",
                        "4. Use the ElevenLabsTools to convert the summary to audio",
                        "Ensure the summary is within the 3000 character limit to avoid ElevenLabs API limits",
                    ],
                    markdown=True, # Markdown mode to print the output of the agent
                    debug_mode=True, # Debug mode to print the output of the agent
                )

                podcast: RunResponse = blog_to_podcast_agent.run(
                    f"Convert the blog content to a podcast: {url}"
                )

                save_dir = "audio_generations"
                os.makedirs(save_dir, exist_ok=True)

                if podcast.audio and len(podcast.audio) > 0:
                    filename = f"{save_dir}/podcast_{uuid4()}.wav"
                    write_audio_to_file(
                        audio=podcast.audio[0].base64_audio,
                        filename=filename
                    )

                    st.success("Podcast generated successfully! 🎧")
                    audio_bytes = open(filename, "rb").read()
                    st.audio(audio_bytes, format="audio/wav")

                    st.download_button(
                        label="Download Podcast",
                        data=audio_bytes,
                        file_name="generated_podcast.wav",
                        mime="audio/wav"
                    )
                else:
                    st.error("No audio was generated. Please try again.")

            except Exception as e:
                st.error(f"An error occurred: {e}")
                logger.error(f"Streamlit app error: {e}")
