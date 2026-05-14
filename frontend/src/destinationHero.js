/**
 * Curated hero imagery by destination keyword (Unsplash, stable IDs).
 * Falls back to a small rotating set from a hash of the name.
 */
const FALLBACK_HEROES = [
  "https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?auto=format&fit=crop&w=2000&q=80",
  "https://images.unsplash.com/photo-1469854523086-cc02fe5d8800?auto=format&fit=crop&w=2000&q=80",
  "https://images.unsplash.com/photo-1488646953014-85cb44e25828?auto=format&fit=crop&w=2000&q=80",
  "https://images.unsplash.com/photo-1476514525535-07fb3b4ae5f1?auto=format&fit=crop&w=2000&q=80",
];

const DESTINATION_ROWS = [
  { keys: ["bali", "ubud", "seminyak"], url: "https://images.unsplash.com/photo-1537996194471-e657df975ab4?auto=format&fit=crop&w=2000&q=80" },
  { keys: ["paris", "france", "lyon"], url: "https://images.unsplash.com/photo-1502602898657-3e91760cbb34?auto=format&fit=crop&w=2000&q=80" },
  { keys: ["tokyo", "kyoto", "osaka", "japan"], url: "https://images.unsplash.com/photo-1540959733332-eab4deabeeaf?auto=format&fit=crop&w=2000&q=80" },
  { keys: ["dubai", "uae", "abu dhabi"], url: "https://images.unsplash.com/photo-1512453979798-5ea266f8880c?auto=format&fit=crop&w=2000&q=80" },
  { keys: ["new york", "nyc", "manhattan"], url: "https://images.unsplash.com/photo-1496442226666-8d4d0e62e6e9?auto=format&fit=crop&w=2000&q=80" },
  { keys: ["london", "uk", "england"], url: "https://images.unsplash.com/photo-1513635269973-5967e7b0b3ca?auto=format&fit=crop&w=2000&q=80" },
  { keys: ["sydney", "melbourne", "australia"], url: "https://images.unsplash.com/photo-1506973035872-a4ec16b8e8d9?auto=format&fit=crop&w=2000&q=80" },
  { keys: ["barcelona", "spain", "madrid"], url: "https://images.unsplash.com/photo-1583422409516-2895a77efded?auto=format&fit=crop&w=2000&q=80" },
  { keys: ["goa", "jaipur", "mumbai", "delhi", "kerala", "india"], url: "https://images.unsplash.com/photo-1524492412937-b28074a5d7da?auto=format&fit=crop&w=2000&q=80" },
  { keys: ["istanbul", "turkey"], url: "https://images.unsplash.com/photo-1524231757912-21f4cc3a83d8?auto=format&fit=crop&w=2000&q=80" },
  { keys: ["santorini", "athens", "greece"], url: "https://images.unsplash.com/photo-1613395877344-13d4c79e4284?auto=format&fit=crop&w=2000&q=80" },
  { keys: ["singapore"], url: "https://images.unsplash.com/photo-1525625293386-3f66f8d866b5?auto=format&fit=crop&w=2000&q=80" },
  { keys: ["cairo", "egypt"], url: "https://images.unsplash.com/photo-1539650116574-75c0c6d73a6e?auto=format&fit=crop&w=2000&q=80" },
  { keys: ["rio", "brazil"], url: "https://images.unsplash.com/photo-1483729558449-99ef09a8c325?auto=format&fit=crop&w=2000&q=80" },
  { keys: ["cape town", "south africa"], url: "https://images.unsplash.com/photo-1516026672322-bc52d61a55d5?auto=format&fit=crop&w=2000&q=80" },
];

function hashPick(str) {
  let h = 0;
  const s = str || "";
  for (let i = 0; i < s.length; i += 1) h = (h << 5) - h + s.charCodeAt(i);
  return Math.abs(h) % FALLBACK_HEROES.length;
}

export function getHeroImageForDestination(destination) {
  const d = (destination || "").trim().toLowerCase();
  if (!d) return FALLBACK_HEROES[0];
  for (const row of DESTINATION_ROWS) {
    if (row.keys.some((k) => d.includes(k))) return row.url;
  }
  return FALLBACK_HEROES[hashPick(d)];
}
