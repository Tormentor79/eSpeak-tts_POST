from flask import Flask, request, send_file
import os
import subprocess

app = Flask(__name__)


@app.route("/tts", methods=["POST"])
def generate_tts():
  # Lee el texto largo directamente del cuerpo (body) del POST
  texto = request.data.decode("utf-8")

  if not texto or not texto.strip():
    texto = "Texto vacío"

  audio_path = "audio.wav"

  try:
    # Ejecuta eSpeak NG para generar el archivo WAV en español
    subprocess.run(
        ["espeak-ng", "-v", "es", "-w", audio_path, texto], check=True
    )
    return send_file(audio_path, mimetype="audio/wav")
  except Exception as e:
    return {"error": str(e)}, 500


@app.route("/")
def home():
  return "Servidor eSpeak activo para Integral Server (Modo POST)"


if __name__ == "__main__":
  port = int(os.environ.get("PORT", 5000))
  app.run(host="0.0.0.0", port=port)
