from flask import Flask, render_template, request, send_file
import qrcode
from io import BytesIO
import datetime

app = Flask(__name__)

# ================== ROUTES ==================

@app.route("/")
def index_default():
    return render_template("index.html", ngay="Chưa có", image_file="default.png")

# Trang index có ngày /dd-mm-yyyy
@app.route("/<date_str>")
def index(date_str):
    try:
        # Parse dd-mm-yyyy -> dd/mm/yyyy
        date_obj = datetime.datetime.strptime(date_str, "%d-%m-%Y")
        ngay_nhap = date_obj.strftime("%d/%m/%Y")
    except:
        ngay_nhap = date_str

    return render_template("index.html", ngay=ngay_nhap, image_file="default.png")

# Trang form nhập ngày để sinh QR
@app.route("/qr", methods=["GET", "POST"])
def qr_form():
    if request.method == "POST":
        new_date = request.form.get("new_date")  # dd/mm/yyyy
        try:
            # Parse dd/mm/yyyy
            date_obj = datetime.datetime.strptime(new_date, "%d/%m/%Y")
            date_str = date_obj.strftime("%d-%m-%Y")  # chuyển thành dd-mm-yyyy
        except:
            date_str = new_date.replace("/", "-")  # fallback

        # Link sản phẩm mà QR sẽ trỏ tới
        url = f"http://127.0.0.1:5000/{date_str}"

        qr_img = qrcode.make(url)
        img_io = BytesIO()
        qr_img.save(img_io, "PNG")
        img_io.seek(0)

        return send_file(img_io, mimetype="image/png")

    return render_template("qr.html")

# ================== RUN ==================
if __name__ == "__main__":
    app.run(debug=True)
