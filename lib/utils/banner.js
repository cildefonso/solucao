const LOGO_LINES = [
   ' _____       _  ',               
   '/  ___|     | | ',                  
   '\ `--.  ___ | |_   _  ___  __ _  ___  ',
   ' `--. \/ _ \| | | | |/ __|/ _` |/ _ \ ',
   '/\__/ / (_) | | |_| | (__| (_| | (_) |',
   '\____/ \___/|_|\__,_|\___|\__,_|\___/ ',
];

const LOGO_COLOR = '#ffa203';
const SIGNATURE_LINE = 5;
const SIGNATURE_MARGIN = 3;

export function clearTerminalForLogo() {
  if (process.stdout.isTTY) {
    process.stdout.write('\x1b[2J\x1b[H');
  }
}

export function renderSolucaoLogo(chalk) {
  const logo = chalk.hex(LOGO_COLOR);
  const maxWidth = Math.max(...LOGO_LINES.map(line => line.length));

  return LOGO_LINES
    .map((line, index) => {
      const logoLine = logo(line.padEnd(maxWidth));

      if (index !== SIGNATURE_LINE) {
        return logoLine;
      }

      return `${logoLine}${' '.repeat(SIGNATURE_MARGIN)}${chalk.white('by cildefonso')}`;
    })
    .join('\n');
}
