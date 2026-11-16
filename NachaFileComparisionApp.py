import streamlit as st
import html
import itertools

st.title("Nacha Files Comparison")

file_a = st.file_uploader("Upload an Nacha File from MF", type="txt")
file_b = st.file_uploader("Upload an Nacha File from GCS", type="txt")

def render_char(char: str) -> str:
    if char == " ":
        return "·"
    if char == "\t":
        return "⇥"
    return html.escape(char)

def highlight_pair_line(line_a: str, line_b: str) -> tuple[str, str]:
    left_html, right_html = [], []
    for char_a, char_b in itertools.zip_longest(line_a, line_b, fillvalue=""):
        rendered_a = render_char(char_a)
        rendered_b = render_char(char_b)
        if char_a != char_b:
            left_html.append(f"<span style='background-color:#ff4d4f;color:white'>{rendered_a or '∅'}</span>")
            right_html.append(f"<span style='background-color:#ff4d4f;color:white'>{rendered_b or '∅'}</span>")
        else:
            left_html.append(rendered_a)
            right_html.append(rendered_b)
    return "".join(left_html), "".join(right_html)

if file_a and file_b:
    text_a = file_a.getvalue().decode("utf-8")
    text_b = file_b.getvalue().decode("utf-8")
    lines_a = [line.rstrip("\r\n") for line in text_a.splitlines()]
    lines_b = [line.rstrip("\r\n") for line in text_b.splitlines()]

    st.subheader("Preview: File A (MF)")
    st.text("\n".join(lines_a[:5]))

    st.subheader("Preview: File B (GCS)")
    st.text("\n".join(lines_b[:5]))

    st.subheader("Comparison (Differences in Red)")
    has_diff = lines_a != lines_b
    if not has_diff:
        st.success("No differences found.")
    else:
        for line_no, (line_a, line_b) in enumerate(itertools.zip_longest(lines_a, lines_b, fillvalue=""), start=1):
            if line_a == line_b:
                continue
            line_a_html, line_b_html = highlight_pair_line(line_a, line_b)
            st.markdown(f"**Line {line_no}**")
            st.markdown("**File A (MF)**")
            st.markdown(f"<pre style='margin:0'>{line_a_html}</pre>", unsafe_allow_html=True)
            st.markdown("**File B (GCS)**")
            st.markdown(f"<pre style='margin:0'>{line_b_html}</pre>", unsafe_allow_html=True)
            st.markdown("---")

else:
    st.info("Please upload both Nacha files to compare.")