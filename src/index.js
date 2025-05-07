import pdf from "pdf-parse";

const MAX_MB    = 4;
const MAX_CHARS = 20000;

async function pdfToText(buf) {
  return (await pdf(Buffer.from(buf))).text
           .replace(/\s+\n/g, "\n")
           .slice(0, MAX_CHARS);
}

export default {
  async fetch(req) {
    if (req.method !== "POST")
      return new Response('POST JSON {"url":"https://…"}', { status: 405 });

    const { url } = await req.json().catch(() => ({}));
    if (!url?.startsWith("http"))
      return new Response("bad url", { status: 400 });

    const res = await fetch(url);
    if (!res.ok) return new Response("url fetch fail", { status: 400 });

    const buf = await res.arrayBuffer();
    if (buf.byteLength > MAX_MB * 1024 * 1024)
      return new Response("file too big", { status: 413 });

    const text = await pdfToText(buf);
    return Response.json({ text, bytes: buf.byteLength });
  }
};