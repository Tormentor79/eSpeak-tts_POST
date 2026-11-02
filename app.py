from flask import Flask, request, send_file
import os
import subprocess

app = Flask(__name__)


@app.route("/tts", methods=["POST"])
def generate_tts():
  # Lee el texto completo del cuerpo del POST
  texto = request.data.decode("utf-8")

  if not texto or not texto.strip():
    texto = "Texto vacío"

  audio_path = "audio.wav"

  try:
    # Ejecutamos eSpeak NG pasándole el texto por stdin (input)
    # Esto evita cualquier límite de tamaño o problemas con puntuación/espacios
    subprocess.run(
        ["espeak-ng", "-v", "es", "-w", audio_path],
        input=texto.encode("utf-8"),
        check=True,
    )

    return send_file(audio_path, mimetype="audio/mpeg")
  except Exception as e:
    return {"error": str(e)}, 500


@app.route("/")
def home():
  return "Servidor eSpeak activo (Modo STDIN)"


if __name__ == "__main__":
  port = int(os.environ.get("PORT", 5000))
  app.run(host="0.0.0.0", port=port)
