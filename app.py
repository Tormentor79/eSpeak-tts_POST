import os
import subprocess
from flask import Flask, request, send_file

app = Flask(__name__)


@app.route("/tts", methods=["POST"])
def generate_tts():
  try:
    # Recibir texto por el cuerpo de la petición POST
    texto = request.data.decode("utf-8")
    if not texto or not texto.strip():
      texto = "Texto vacío"

    audio_path = "audio.wav"

    # Ejecutar espeak-ng mediante entrada estándar (stdin)
    resultado = subprocess.run(
        ["espeak-ng", "-v", "es", "-w", audio_path],
        input=texto.encode("utf-8"),
        capture_output=True,
        text=False,
    )

    if resultado.returncode != 0:
      error_msg = resultado.stderr.decode("utf-8", errors="ignore")
      print(f"Error en espeak-ng: {error_msg}")
      return {"error": f"espeak falló: {error_msg}"}, 500

    return send_file(audio_path, mimetype="audio/wav")

  except Exception as e:
    print(f"Excepción crítica en eSpeak: {str(e)}")
    return {"error": str(e)}, 500


@app.route("/", methods=["GET"])
def home():
  return "Servidor eSpeak (Docker) activo y listo para recibir POST.", 200


if __name__ == "__main__":
  port = int(os.environ.get("PORT", 5000))
  app.run(host="0.0.0.0", port=port)
