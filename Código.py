
# -----------------------------------------------------------------
# PASO 2: Procesar anuncios de Facebook aplicando categorías
# -----------------------------------------------------------------
print("\n" + "="*55)
print(" [Scraping FB] Analizando Fuente 2 (Facebook Marketplace) ")
print("="*55)

soup_fb = BeautifulSoup(html_facebook, 'html.parser')
titulos_fb = soup_fb.find_all('h1', class_='fb-title')
precios_fb = soup_fb.find_all('div', class_='fb-price')

for i in range(len(titulos_fb)):
    titulo_fb = titulos_fb[i].text
    precio_fb = limpiar_precio(precios_fb[i].text)
    categoria_fb = obtener_categoria(titulo_fb)

    print(f"\n-> Anuncio {i+1}: '{titulo_fb}'")
    print(f"   Categoría detectada: {categoria_fb} | Precio publicado: S/ {precio_fb}")

    if categoria_fb == "No identificado" or categoria_fb not in umbrales_por_categoria:
        print("   ⚠️ NO SE PUEDE EVALUAR: El anuncio no posee suficientes palabras clave de validación.")
    else:
        umbral_aplicable = umbrales_por_categoria[categoria_fb]["critico"]
        if precio_fb < umbral_aplicable:
            print(f"   🚨 FRAUDE DETECTADO: El precio es demasiado bajo para la categoría '{categoria_fb}'.")
        else:
            print(f"   ✅ ANUNCIO SEGURO: El precio coincide con el mercado para un(a) '{categoria_fb}'.")

# -----------------------------------------------------------------
# PASO 3: INTERFAZ INTERACTIVA INTELIGENTE
# -----------------------------------------------------------------
print("\n" + "="*55)
print(" 🕵️‍♂️ MÓDULO DE CONSULTA MANUAL PARA EL USUARIO 🕵️‍♂️")
print("="*55)

while True:
    print("\n¿Viste otro anuncio sospechoso en redes sociales?")
    entrada_titulo = input("👉 Ingresa el TÍTULO del anuncio (o 'salir'): ")

    if entrada_titulo.lower() == 'salir':
        print("\n¡Gracias por usar el Sistema de Detección de Fraude (LP)!")
        break

    entrada_precio = input("👉 Ingresa el PRECIO que viste (solo números): ")

    try:
        precio_consultado = float(entrada_precio)
        categoria_detectada = obtener_categoria(entrada_titulo)

        # VALIDACIÓN DEFENSIVA GLOBAL
        if categoria_detectada == "No identificado" or categoria_detectada not in umbrales_por_categoria:
            print(f"\n❌ El sistema no pudo reconocer o no tiene datos de referencia para '{entrada_titulo}'.")
            print("   Por favor, asegúrate de incluir palabras clave como 'Consola', 'PS5', 'Mando' o 'Juego'.")
        else:
            datos_mercado = umbrales_por_categoria[categoria_detectada]
            print(f"\n[Analizando...] Producto detectado como: {categoria_detectada}")

            if precio_consultado < datos_mercado["critico"]:
                print(f"🚨 ALERTA CRÍTICA: S/ {precio_consultado} es una estafa casi segura.")
                print(f"   Un(a) {categoria_detectada} original formal no baja de S/ {datos_mercado['minimo']}.")
            else:
                print(f"✅ VERIFICADO: El precio es coherente para un(a) {categoria_detectada}.")

    except ValueError:
        print("❌ Error: Ingresa solo números en el campo de precio.")