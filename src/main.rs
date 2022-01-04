use actix_web::{web, App, HttpServer};
use actix_files as fs;
mod cli;
mod lobby;


#[actix_web::main]
async fn main() -> std::io::Result<()> {
    let args = cli::parse_args();
    let listen = args.flag_listen;
    let server = move || {
        let mut app = App::new();
        if args.cmd_web {
            app = app.service(web::resource("/ws").route(web::get().to(lobby::entrance)))
        } else if args.cmd_server {
            app = app.service(fs::Files::new("/", args.flag_dir.as_str()).index_file("index.html"))
        }
        return app;
    };
    HttpServer::new(server)
        .bind(&listen)?
        .run()
        .await
}