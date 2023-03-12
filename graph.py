import io
import base64

import matplotlib
matplotlib.use('Agg')   # Para multi-thread, non-interactive backend (avoid run in main loop)
import matplotlib.pyplot as plt
# Para convertir matplotlib a imagen y luego a datos binarios
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.image as mpimg


def graficar(users, titles_ap):
        
    fig = plt.figure()
    fig.suptitle('usuario vs titulos completados', fontsize=16)
    ax = fig.add_subplot()
    ax.bar(users, titles_ap, label='titulos completados')
    ax.set_facecolor('whitesmoke')
    ax.legend()
  
    # Convertir ese grafico en una imagen para enviar por HTTP y mostrar en el HTML
    image_html = io.BytesIO()
    FigureCanvas(fig).print_png(image_html)
    plt.close(fig)  # Cerramos la imagen para que no consuma memoria del sistema
    return image_html