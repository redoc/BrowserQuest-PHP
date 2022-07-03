use actix::{Actor, StreamHandler};
use actix_web::{web, Error, HttpRequest, HttpResponse};
use actix_web_actors::ws;
use actix::ActorContext; 
use std::collections::HashMap;

// use actix_web::{web, App, HttpServer};
// use super::args;


pub async fn entrance(req: HttpRequest, stream: web::Payload) -> Result<HttpResponse, Error> {
    let  conn = session::Connection::new();
    let resp = ws::start(conn, &req, stream);
    
    println!("{:?}", resp);
    return resp;
}

pub struct LobbyServer {
    id: String,
    sessions: HashMap<i32, Box<session::Connection>>,
}

impl LobbyServer {
    fn new(id: &str) -> Self {
        Self {
            id: String::from(id),
            sessions: HashMap::new(),
        }
    }
}

impl Actor for LobbyServer {
    type Context = ws::WebsocketContext<Self>;
    fn started(&mut self, _ctx: &mut Self::Context) {
        println!("hello {0}", self.id);
    }
}

impl StreamHandler<Result<ws::Message, ws::ProtocolError>> for LobbyServer {
    fn handle(
        &mut self,
        msg: Result<ws::Message, ws::ProtocolError>,
        ctx: &mut Self::Context,
    ) {
        match msg {
            Ok(ws::Message::Ping(msg)) => {
                ctx.pong(&msg);
            }

            Ok(ws::Message::Text(text)) => {
                ctx.text(text);
            }

            Ok(ws::Message::Binary(bin)) => {
                ctx.binary(bin);
            }

            Ok(ws::Message::Close(reason)) => {
                ctx.close(reason);
                ctx.stop();
            }
            _ => {
                ctx.stop();
            }
        }
    }
}

mod session {
    use actix::{Actor, StreamHandler};
    use actix_web_actors::ws;
    use actix::ActorContext;
    use std::sync::atomic::AtomicU32;
    use std::sync::atomic::Ordering;
    static C: AtomicU32 = AtomicU32::new(0);

    pub struct Connection {
        id: u32,
    }

    impl Connection {
        pub fn new() -> Self {
            Self {
                id: C.fetch_add(1, Ordering::SeqCst),
            }
        }
    }

    impl Actor for Connection {
        type Context = ws::WebsocketContext<Self>;
        fn started(&mut self, _ctx: &mut Self::Context) {
            println!("started connection {0}", self.id);
        }
    }

    impl StreamHandler<Result<ws::Message, ws::ProtocolError>> for Connection {
        fn handle(
            &mut self,
            msg: Result<ws::Message, ws::ProtocolError>,
            ctx: &mut Self::Context,
        ) {
            match msg {
                Ok(ws::Message::Ping(msg)) => {
                    ctx.pong(&msg);
                }

                Ok(ws::Message::Text(text)) => {
                    ctx.text(text);
                }

                Ok(ws::Message::Binary(bin)) => {
                    ctx.binary(bin);
                }

                Ok(ws::Message::Close(reason)) => {
                    ctx.close(reason);
                    ctx.stop();
                }
                _ => {
                    println!("broken connection {0}", self.id);
                    ctx.stop();
                }
            }
        }
    }
}
