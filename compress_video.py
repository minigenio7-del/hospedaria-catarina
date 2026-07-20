import os
import subprocess
import sys

def compress_video():
    project_dir = os.path.dirname(os.path.abspath(__file__))
    input_video = os.path.join(project_dir, 'fotos', 'vista area.mp4')
    output_video = os.path.join(project_dir, 'fotos', 'vista area optimized.mp4')
    
    if not os.path.exists(input_video):
        print(f"Vídeo de entrada não encontrado em: {input_video}")
        return

    print("=== Otimizador de Vídeo da Hospedaria ===")
    print(f"Vídeo original: {input_video} ({os.path.getsize(input_video)/(1024*1024):.2f} MB)")
    
    # Verifica se o FFmpeg está instalado
    try:
        subprocess.run(['ffmpeg', '-version'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("FFmpeg detectado no sistema! Iniciando a compressão...")
    except FileNotFoundError:
        print("\n[AVISO] FFmpeg não foi encontrado no PATH do sistema.")
        print("Para comprimir o vídeo no seu computador, você pode:")
        print("1. Instalar o FFmpeg (via winget: 'winget install Gyan.FFmpeg' no terminal)")
        print("2. Ou usar uma ferramenta online grátis como: https://www.freeconvert.com/video-compressor")
        print("3. Ou usar o site: https://clideo.com/compress-video")
        print("\nCaso consiga rodar com FFmpeg instalado, execute este script novamente.")
        return

    # Comando FFmpeg para compressão ultra-otimizada (Codec H.264, CRF 28 - excelente balanço entre qualidade e tamanho)
    cmd = [
        'ffmpeg',
        '-y',               # Sobrescreve sem perguntar
        '-i', input_video,  # Entrada
        '-vcodec', 'libx264',
        '-crf', '28',       # Fator de compressão (23 é padrão, 28 é bem menor mantendo boa qualidade)
        '-preset', 'slow',  # Compressão mais eficiente
        '-an',              # Remove áudio (vídeo de fundo não precisa de som)
        output_video        # Saída
    ]
    
    try:
        print("Executando compressão do vídeo... Isso pode levar alguns segundos.")
        subprocess.run(cmd, check=True)
        
        orig_size = os.path.getsize(input_video)
        opt_size = os.path.getsize(output_video)
        
        # Se deu certo, renomeia o original como backup e o novo como oficial
        backup_video = os.path.join(project_dir, 'fotos', 'vista area.mp4.bak')
        if os.path.exists(backup_video):
            os.remove(backup_video)
            
        os.rename(input_video, backup_video)
        os.rename(output_video, input_video)
        
        print("\n=== SUCESSO! ===")
        print(f"Vídeo original salvo como: {backup_video}")
        print(f"Vídeo otimizado substituído em: {input_video}")
        print(f"Tamanho anterior: {orig_size/(1024*1024):.2f} MB")
        print(f"Tamanho atual: {opt_size/(1024*1024):.2f} MB")
        print(f"Economia de: {(orig_size - opt_size)/(1024*1024):.2f} MB (Redução de {((orig_size-opt_size)/orig_size)*100:.1f}%)")
        
    except Exception as e:
        print(f"Erro ao processar o vídeo: {e}")

if __name__ == '__main__':
    compress_video()
