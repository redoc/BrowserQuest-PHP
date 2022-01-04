use docopt::Docopt;
use serde::Deserialize;

const USAGE: &'static str = "
Zero

Usage:
zero web     [--listen=<addr>] --dir=<dir>
zero server  [--listen=<addr>]
zero --version
zero (-h | --help)

Options:
-h --help           Show usage.
--version           Show version.
--listen=<addr>     TCP address [default: 0.0.0.0:9527].
--dir=<dir>         Directory of static files.
";

#[derive(Debug, Deserialize)]
pub struct Args {
    pub flag_listen: String,
    pub flag_dir: String,
    pub cmd_web: bool,
    pub cmd_server: bool,
}

pub fn parse_args() -> Args {
    let args: Args = Docopt::new(USAGE)
        .and_then(|d| d.deserialize())
        .unwrap_or_else(|e| e.exit());
    println!("{:?}", args);
    return args;
}