mod lobby;
mod cli;


#[actix_web::main]
async fn main() -> std::io::Result<()> {
    let args = cli::args::parse();
    println!("cli args: {:?}", args);
    if args.cmd_web {
        return cli::web::run(&args).await;
    } else if args.cmd_lobby {
        return cli::lobby::run(&args).await;
    } else {
        panic!("missing subcommand");
    }
}