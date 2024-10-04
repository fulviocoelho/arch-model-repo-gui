const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');
const { rimraf } = require('rimraf');

async function removePastaTemp(projectDir) {
    try {
      console.log('Removendo a pasta temporária...');
      const tempDir = projectDir;
    //   await rimraf(tempDir, { force: true }); // Tenta remover com força
  
      // Se o rimraf falhar, tenta remover com o comando do sistema
      try {
        await rimraf(tempDir, { force: true });
      } catch (err) {
        console.error(`Erro ao remover a pasta temporária: ${err.message}`);
        // Tenta remover com o comando do sistema (sincronamente)
        if (process.platform === 'win32') {
          execSync(`del /f /s /q "${tempDir}"`); // Windows
        } else {
          execSync(`rm -rf "${tempDir}"`); // Linux/macOS
        }
      }
    } catch (error) {
      console.error(`Erro ao remover a pasta temporária: ${error.message}`);
    }
  }
  
  // Exemplo de uso:
  const caminhoPastaAtual = path.dirname(process.argv[1]);
  
  // Remove a pasta temporária antes de iniciar a atualização
  const tempDir = path.join(caminhoPastaAtual, 'project-repo');
  if (fs.existsSync(tempDir)) {
    // Aguarda 3 segundos antes de tentar remover a pasta temporária novamente
    setTimeout(() => {
      removePastaTemp(tempDir);
    }, 3000);
  }