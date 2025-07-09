import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import { useMemo } from 'react';
import { MapContainer, Marker, Popup, TileLayer, useMap } from 'react-leaflet';
import type { ILocation } from '../../types';

interface IProps {
  items: Omit<ILocation, "id">[];
}

const ItemsMap = ({ items }: IProps) => {
  
  const center: [number, number] = useMemo(() => [Number(items[0].lat), Number(items[0].lng)], [items]);
  
  if (!items.length) return <div>No items to display</div>;


  if ((L.Icon.Default.prototype as unknown as { _getIconUrl?: unknown })._getIconUrl) {
    delete (L.Icon.Default.prototype as unknown as { _getIconUrl?: unknown })._getIconUrl;
  }
  L.Icon.Default.mergeOptions({
    iconRetinaUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png',
    iconUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png',
    shadowUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png',
  });

  function SetViewOnClick({ coordinates }: { coordinates: [number, number] }) {
    const map = useMap();
    map.setView(coordinates, map.getZoom());
    return null;
  }

  return (
    // @ts-expect-error 'center' is a valid prop at runtime for MapContainer, but not in the current type definitions
    <MapContainer center={center} zoom={13} style={{ height: '400px', width: '100%' }}>
      <SetViewOnClick coordinates={center} />
      <TileLayer
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />
      {items.map((item, idx) => (
        <Marker key={idx} position={[item.lat, item.lng]}>
          <Popup>
            <div className="flex flex-col gap-1">
              <span className="font-bold">
                {item?.address}, {item?.city}, {item?.state}, {item?.country_code}
              </span>
              <span className="">
                Lat: {item?.lat}, Lng: {item?.lng}
              </span>
            </div>
          </Popup>
        </Marker>
      ))}
    </MapContainer>
  );
}

export default ItemsMap;