export default function handler(req, res) {
  const apiKey =
    process.env.NEXT_PUBLIC_GOOGLE_MAPS_API_KEY ||
    process.env.GOOGLE_MAPS_API_KEY ||
    '';
  const mapId =
    process.env.NEXT_PUBLIC_GOOGLE_MAPS_MAP_ID ||
    process.env.GOOGLE_MAPS_MAP_ID ||
    '';

  res.setHeader('Content-Type', 'application/json; charset=utf-8');
  res.setHeader('Cache-Control', 'public, s-maxage=3600, stale-while-revalidate=86400');
  return res.status(200).json({ apiKey, mapId });
}
