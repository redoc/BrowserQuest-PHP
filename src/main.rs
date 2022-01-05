// use log::{info};
use std::process;
use std::path::Path;
use actix_web::{web, App, HttpServer};
use actix_files as fs;
mod cli;
mod lobby;


#[actix_web::main]
async fn main() -> std::io::Result<()> {
    let args = cli::parse_args();
    let listen = args.flag_listen.clone();
    let static_dir = args.flag_static.clone();
    if !(Path::new(&static_dir).is_dir()) {
        println!("static directory '{}' does'nt exist. plz recheck your '--static'", static_dir);
        process::exit(1);
    }
    let server = move || {
        let mut app = App::new();
        if args.cmd_server {
            app = app.service(web::resource("/ws").route(web::get().to(lobby::entrance)))
        } else if args.cmd_web {
            app = app.service(fs::Files::new("/", static_dir.as_str()).index_file("index.html"))
        }
        return app;
    };

    if args.cmd_server {
        println!("started lobby listening:{}", listen);
    } else if args.cmd_web {
        println!("started web   listening:{} static_dir={}", listen, args.flag_static);
    }
    HttpServer::new(server)
        .bind(&args.flag_listen)?
        .run()
        .await
}