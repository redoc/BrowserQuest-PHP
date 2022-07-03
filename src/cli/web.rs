use actix_web::{App, HttpServer};
use actix_files as fs;
use super::args;

pub async fn run(args: &args::Args) -> std::io::Result<()> {
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