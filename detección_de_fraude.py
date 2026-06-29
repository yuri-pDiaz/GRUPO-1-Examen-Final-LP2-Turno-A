# -----------------------------------------------------------------
# PASO 1: Procesar y Segmentar el Mercado Formal (ML)
# -----------------------------------------------------------------
soup_ml = BeautifulSoup(html_mercado_libre, 'html.parser')
titulos_ml = soup_ml.find_all('h2', class_='titulo-prod')
precios_ml = soup_ml.find_all('span', class_='precio-prod')

datos_segmentados = {
    "Consola Estándar": [],
    "Consola + Mando": [],
    "Consola + Juego": []
}

print("[Scraping ML] Extrayendo y segmentando el mercado:")

for i in range(len(titulos_ml)):
    titulo = titulos_ml[i].text
    precio = limpiar_precio(precios_ml[i].text)

    if precio < 1500:
        print(f"   -> 🗑️ [RUIDO DESCARTADO] {titulo[:35]}... (S/ {precio})")
    else:
        categoria = obtener_categoria(titulo)
        # VALIDACIÓN DEFENSIVA: Evita que el programa colapse si devuelve 'No identificado'
        if categoria in datos_segmentados:
            datos_segmentados[categoria].append(precio)
            print(f"   -> 📦 [GUARDADO EN: {categoria}] {titulo[:30]}... | S/ {precio}")
        else:
            print(f"   -> ⚠️ [IGNORADO - NO CATEGORIZADO] {titulo[:30]}... | S/ {precio}")

# Calcular métricas seguras
umbrales_por_categoria = {}
print("\n📊 MÉTRICAS CALCULADAS POR CATEGORÍA:")

for cat, lista_precios in datos_segmentados.items():
    if len(lista_precios) > 0:
        minimo = min(lista_precios)
        promedio = sum(lista_precios) / len(lista_precios)
        critico = minimo * 0.60

        umbrales_por_categoria[cat] = {"minimo": minimo, "promedio": promedio, "critico": critico}
        print(f" * {cat}: Promedio S/{promedio:.0f} | Mínimo Seguro S/{minimo} | Umbral Riesgo S/{critico:.0f}")
