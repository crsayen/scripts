use std::io::{stdin, stdout, Result, Write};
use std::time::Instant;
use termion::event::Key;
use termion::input::TermRead;
use termion::raw::IntoRawMode;

fn main() {
    let stdin = stdin();
    let mut stdout = stdout().into_raw_mode().unwrap();
    let mut text = String::new();
    let mut started: bool = false;
    let mut start = Instant::now();
    let mut duration: u128 = 0;

    prompt().unwrap();

    for c in stdin.keys() {
        if !started {
            start = Instant::now();
            started = true;
        }

        match c.unwrap() {
            Key::Char('\n') => {
                started = false;
                let nwords = text.split_ascii_whitespace().count();
                results_and_prompt(&nwords, &duration).unwrap();
                text.clear();
            }
            Key::Ctrl('q') => break,
            Key::Backspace => {
                text.truncate(if text.len() > 0 { text.len() - 1 } else { 0 });
                render_text(&text);
            }
            Key::Char('\t') => text.push(' '),
            Key::Char(k) => {
                duration = start.elapsed().as_millis();
                text.push(k);
                render_text(&text);
            }
            _ => (),
        }

        stdout.flush().unwrap();
    }
}

fn prompt() -> Result<()> {
    let mut stdout = stdout().into_raw_mode().unwrap();
    return write!(
        stdout,
        r#"{}{}start typing to begin. Hit enter when finished. ctrl + q to quit."#,
        termion::cursor::Goto(1, 1),
        termion::clear::All
    );
}

fn results_and_prompt(nwords: &usize, millis: &u128) -> Result<()> {
    let mut stdout = stdout().into_raw_mode().unwrap();
    let seconds = millis / 1000;
    let remainder = (millis % 1000) / 100;
    let wpm = ((600000000000 / millis) * u128::try_from(*nwords).unwrap()) / 10000000;
    return write!(
        stdout,
        "{}{}you typed {} words in {}.{} seconds{}{} WPM{}start typing to begin. Hit enter when finished. ctrl + q to quit.{}",
        termion::cursor::Goto(1, 1),
        termion::clear::All,
        nwords,
        seconds,
        remainder,
        termion::cursor::Goto(1, 2),
        wpm,
        termion::cursor::Goto(1, 3),
        termion::cursor::Goto(1, 4),
    );
}

fn render_text(text: &String) {
    let mut stdout = stdout().into_raw_mode().unwrap();
    write!(
        stdout,
        "{}{}{}",
        termion::cursor::Goto(1, 1),
        termion::clear::All,
        text,
    )
    .unwrap();
}
