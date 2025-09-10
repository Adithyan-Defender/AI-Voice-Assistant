import speedtest
from Mouth import speak  # Ensure you have a speak function

def get_internet_speed():
    """Check internet speed using Speedtest API."""
    try:
        speak("Checking your internet speed, please wait...")
        
        st = speedtest.Speedtest()
        st.get_best_server()  # Find the closest, fastest server

        # ✅ Measure speeds
        download_speed = st.download() / 1_000_000  # Convert to Mbps
        upload_speed = st.upload() / 1_000_000  # Convert to Mbps
        ping = st.results.ping  # Get ping in ms

        # ✅ Format results
        result_text = (
            f"Download: {download_speed:.2f} Mbps, "
            f"Upload: {upload_speed:.2f} Mbps, "
            f"Ping: {ping} ms"
        )

        return result_text

    except Exception as e:
        return f"Error: {str(e)}"

def check_internet_speed():
    """Retrieves and announces the internet speed."""
    speed_result = get_internet_speed()

    if "Error" not in speed_result:
        speak(f"Sir, your internet speed is {speed_result}.")
    else:
        speak("Error: Unable to retrieve internet speed.")

