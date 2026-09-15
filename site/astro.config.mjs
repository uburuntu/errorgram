import { defineConfig } from "astro/config";
import starlight from "@astrojs/starlight";

export default defineConfig({
  site: "https://errorgram.rmbk.me",
  output: "static",
  trailingSlash: "always",
  integrations: [
    starlight({
      title: "Errorgram",
      description: "Precise Telegram Bot API errors for Python, TypeScript, aiogram, and grammY.",
      logo: { src: "./src/assets/mark.svg" },
      favicon: "/favicon.svg",
      social: [
        {
          icon: "github",
          label: "Errorgram on GitHub",
          href: "https://github.com/uburuntu/errorgram",
        },
      ],
      editLink: {
        baseUrl: "https://github.com/uburuntu/errorgram/edit/main/site/",
      },
      customCss: ["./src/styles/custom.css"],
      sidebar: [
        { label: "Overview", slug: "" },
        { label: "Get started", slug: "getting-started" },
        {
          label: "Use Errorgram",
          items: [
            { label: "Python & aiogram", slug: "python" },
            { label: "JavaScript & grammY", slug: "javascript" },
            { label: "How matching works", slug: "matching" },
          ],
        },
        { label: "Browse the catalogue", slug: "catalogue" },
        {
          label: "Error reference",
          items: [{ autogenerate: { directory: "errors" } }],
          collapsed: false,
        },
        {
          label: "Keep it useful",
          items: [
            { label: "For AI agents", slug: "agents" },
            { label: "Contribute a condition", slug: "contributing" },
            { label: "Follow upstream changes", slug: "updating" },
          ],
        },
      ],
    }),
  ],
});
