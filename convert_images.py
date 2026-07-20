import os
import sys

try:
    from PIL import Image
except ImportError:
    print("Biblioteca 'Pillow' nao encontrada. Instalando...")
    os.system(f"{sys.executable} -m pip install Pillow")
    from PIL import Image

def convert_to_webp():
    target_dir = os.path.join(os.path.dirname(__file__), 'fotos')
    if not os.path.exists(target_dir):
        print(f"Diretorio {target_dir} nao encontrado!")
        return

    print("=== Otimizando Imagens para WebP ===")
    files = os.listdir(target_dir)
    total_saved = 0

    for file in files:
        if file.lower().endswith(('.png', '.jpg', '.jpeg')):
            file_path = os.path.join(target_dir, file)
            name, ext = os.path.splitext(file)
            
            # Pula o video do hero
            if name == "vista area" and ext.lower() == ".mp4":
                continue
                
            webp_path = os.path.join(target_dir, f"{name}.webp")
            
            try:
                # Abre e comprime
                img = Image.open(file_path)
                original_size = os.path.getsize(file_path)
                
                # Trata imagem RGBA para RGB se for JPG
                if img.mode in ('RGBA', 'LA'):
                    background = Image.new('RGBA', img.size, (255, 255, 255))
                    alpha_composite = Image.alpha_composite(background, img)
                    img = alpha_composite.convert('RGB')
                
                # Salva como WebP
                img.save(webp_path, 'WEBP', quality=80)
                webp_size = os.path.getsize(webp_path)
                
                saved = original_size - webp_size
                total_saved += saved
                
                print(f"Otimizado: {file} ({original_size/1024:.1f}KB) -> {name}.webp ({webp_size/1024:.1f}KB) | Economia: {saved/1024:.1f}KB")
            except Exception as e:
                print(f"Erro ao processar {file}: {e}")
            
    print(f"\nConcluido! Economia total estimada: {total_saved/(1024*1024):.2f} MB")

if __name__ == '__main__':
    convert_to_webp()
