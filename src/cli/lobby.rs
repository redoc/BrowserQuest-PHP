use actix_web::{web, App, HttpServer};
use super::args;
use super::super::lobby;

pub async fn run(args: &args::Args) -> std::io::Result<()> {
    let listen = args.flag_listen.clone();
    let server = move || {
        let mut app = App::new();
        app = app.service(web::resource("/ws").route(web::get().to(lobby::entrance)));
        return app;
    };
    HttpServer::new(server)
        .bind(&listen)?
        .run()
        .await
}