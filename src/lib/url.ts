/** Prefix a site path with the base path (for example /chord-site/). */
export function url(path = ''): string {
	const base = import.meta.env.BASE_URL.replace(/\/$/, '');
	const clean = path.replace(/^\//, '');
	return `${base}/${clean}`;
}
