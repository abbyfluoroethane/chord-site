// @ts-check
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';

const fonts =
	'https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,700&family=IBM+Plex+Mono:wght@400&family=IBM+Plex+Sans:wght@400;500;600&display=swap';

// https://astro.build/config
export default defineConfig({
	site: 'https://chordapp.foid.space',
	integrations: [
		starlight({
			title: 'Chord',
			logo: {
				light: './src/assets/chord-mark-light.svg',
				dark: './src/assets/chord-mark-dark.svg',
			},
			favicon: '/favicon.svg',
			customCss: ['./src/styles/starlight.css', './src/styles/shots.css'],
			head: [{ tag: 'link', attrs: { rel: 'stylesheet', href: fonts } }],
			social: [
				{ icon: 'github', label: 'GitHub', href: 'https://github.com/abbyfluoroethane/chord-site' },
			],
			sidebar: [
				{
					label: 'Docs',
					items: [
						{ label: 'Overview', slug: 'docs' },
						{ label: 'Getting started', slug: 'docs/getting-started' },
						{ label: 'Find a server', slug: 'docs/find-a-server' },
						{ label: 'Self-host', slug: 'docs/self-host' },
					],
				},
			],
		}),
	],
});
