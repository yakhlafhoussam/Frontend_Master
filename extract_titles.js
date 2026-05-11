import fs from 'fs/promises';
import path from 'path';

const root = process.cwd();

function extractFirstSentence(content) {
  const lines = content.split('\n');
  for (const line of lines) {
    const trimmed = line.trim();
    if (trimmed && !trimmed.match(/^(WEBVTT|NOTE|REGION|STYLE|-->/)) && !trimmed.match(/^\d+$/)) {
      return trimmed.replace(/<[^>]+>/g, '').replace(/&[a-z]+;/g, '').trim();
    }
  }
  return '';
}

async function main() {
  const playlists = ['playlist_1', 'playlist_2', 'playlist_3', 'playlist_4', 'playlist_5'];
  
  for (const pl of playlists) {
    const dir = path.join(root, pl);
    const files = await fs.readdir(dir);
    const vttFiles = files.filter(f => f.endsWith('.vtt') && !f.includes('.ar.') && !f.includes('.fr.')).sort();
    
    console.log(`\n=== ${pl} (${vttFiles.length} videos) ===`);
    for (const vtt of vttFiles.slice(0, 5)) {
      const content = await fs.readFile(path.join(dir, vtt), 'utf8');
      const firstLine = extractFirstSentence(content);
      console.log(`${vtt.slice(0, 50)}: ${firstLine.slice(0, 80)}`);
    }
  }
}

main().catch(console.error);
