import argparse
import ipaddress
import sys


def parse_route_line(line):
    """'ip route CIDR IFACE auto !COMMENT' -> (network, iface, comment) or None"""
    line = line.strip()
    if not line or not line.startswith('ip route '):
        return None
    parts = line.split(None, 5)
    if len(parts) < 3:
        return None
    cidr = parts[2]
    iface = parts[3] if len(parts) > 3 else ''
    auto = parts[4] if len(parts) > 4 else ''
    comment = parts[5] if len(parts) > 5 else ''
    try:
        network = ipaddress.ip_network(cidr, strict=False)
    except ValueError:
        return None
    return network, iface, auto, comment


def merge_routes(files):
    routes = {}  # network -> (iface, auto, comment)
    per_file_counts = []

    for filepath in files:
        count = 0
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                for line in f:
                    result = parse_route_line(line)
                    if result:
                        count += 1
                        if result[0] not in routes:
                            net, iface, auto, comment = result
                            routes[net] = (iface, auto, comment)
        except Exception as e:
            print(f"Ошибка чтения {filepath}: {e}", file=sys.stderr)
        per_file_counts.append((filepath, count))

    # Сортируем по длине префикса по возрастанию (сначала крупные сети)
    all_networks = sorted(routes.keys(), key=lambda n: n.prefixlen)

    kept = []
    for net in all_networks:
        if not any(net.subnet_of(k) for k in kept):
            kept.append(net)

    kept.sort(key=lambda n: (n.network_address, n.prefixlen))
    return [(net, routes[net]) for net in kept], per_file_counts


def main():
    parser = argparse.ArgumentParser(
        description='Объединяет файлы маршрутов Keenetic, убирает дубли и подсети.'
    )
    parser.add_argument('files', nargs='+', help='Входные файлы маршрутов')
    parser.add_argument('-o', '--output', default='merged-routes.txt',
                        help='Выходной файл (по умолчанию: merged-routes.txt)')
    args = parser.parse_args()

    routes, per_file_counts = merge_routes(args.files)

    total_before = sum(c for _, c in per_file_counts)
    print("Входные файлы:")
    for filepath, count in per_file_counts:
        print(f"  {filepath}: {count} записей")
    print(f"  Итого: {total_before} записей\n")

    with open(args.output, 'w', encoding='utf-8') as f:
        for net, (iface, auto, comment) in routes:
            parts = ['ip route', str(net), iface, auto, comment]
            f.write(' '.join(p for p in parts if p) + '\n')

    total_after = len(routes)
    print(f"Результат: {total_after} записей → {args.output}")
    print(f"Удалено: {total_before - total_after} записей (дубли и покрытые подсети)")


if __name__ == '__main__':
    main()
