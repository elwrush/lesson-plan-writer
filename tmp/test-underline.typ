#set page(paper: "a4", margin: 2cm)
#set text(font: "Roboto", size: 11pt)

=== Test 1: Original underline with h() ===

1. Women shown as the #underline(h(3.5cm))

=== Test 2: Explicit stroke underline ===

2. Women shown as the #underline(stroke: 0.5pt + black)[#h(3.5cm)]

=== Test 3: box with bottom stroke ===

3. Women shown as the #box(width: 3.5cm, stroke: (bottom: 0.5pt + black))

=== Test 4: line() function ===

4. Women shown as the #line(length: 3.5cm, stroke: 0.5pt + black)

=== Test 5: line() on its own line ===

5. Women shown as the \
#line(length: 3.5cm, stroke: 0.5pt + black)
