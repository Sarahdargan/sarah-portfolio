title: Building a Kanban Board Without a Framework
date: 2026-04-20
tags: javascript, css

I wanted to understand drag and drop at the DOM level before reaching for a
library, so TaskFlow uses nothing but vanilla JavaScript.

## Drag events, not a library

The HTML Drag and Drop API is clunky but honest: `dragstart`, `dragover`, and
`drop` are enough to move a card between columns once you remember to call
`preventDefault` on `dragover`.

## Where CSS grid helped

Each column is a grid track, and cards inside a column are a simple flex
stack. That combination made reordering feel natural without any JavaScript
layout math.

## What I'd do differently

Local storage persistence works, but it doesn't sync across tabs. A small
`storage` event listener would fix that in an afternoon next on the list.
