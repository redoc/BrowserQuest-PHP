use actix_web::{web, App, HttpServer};
use actix_files as fs;
use docopt::Docopt;
use serde::Deserialize;

#[path="service/lobby.rs"]
mod lobby;

const USAGE: &'static str = "
Zero

Usage:
zero web    [--listen=<addr>] --root-dir=<dir>
zero lobby  [--listen=<addr>]
zero --version
zero (-h | --help)

Options:
-h --help           Show usage.
--version           Show version.
--listen=<addr>     TCP address [default: 0.0.0.0:9527].
--root-dir=<dir>    Directory of static files.
";

#[derive(Debug, Deserialize)]
pub struct Args {
    pub flag_listen: String,
    pub flag_root_dir: String,
    pub cmd_web: bool,
    pub cmd_lobby: bool,
}

pub fn parse() -> Args {
    let args: Args = Docopt::new(USAGE)
        .and_then(|d| d.deserialize())
        .unwrap_or_else(|e| e.exit());
    return args;
}


pub async fn start_lobby(args: &Args) -> std::io::Result<()> {
    let listen = args.flag_listen.clone();
    let server = move || {
        let mut app = App::new();
        app = app.service(web::resource("/").route(web::get().to(lobby::entrance)));
        return app;
    };
    HttpServer::new(server)
        .bind(&listen)?
        .run()
        .await
}


pub async fn start_web(args: &Args) -> std::io::Result<()> {
    let listen = args.flag_listen.clone();
    let _root_dir: String = args.flag_root_dir.clone();
    let server = move || {
        let mut app = App::new();
        app = app.service(fs::Files::new("/", _root_dir.as_str()).index_file("index.html"));
        return app;
    };
    HttpServer::new(server)
        .bind(&listen)?
        .run()
        .await
}
