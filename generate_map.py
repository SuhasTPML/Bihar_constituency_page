import json

# Read and return the SVG file content
def read_svg_file(svg_path):
    with open(svg_path, 'r', encoding='utf-8') as f:
        return f.read()

# Read and return the JSON file content
def read_json_file(json_path):
    with open(json_path, 'r', encoding='utf-8') as f:
        return json.load(f)

# Create an interactive HTML map using the SVG and constituency data
def create_interactive_map(svg_content, constituency_data):
    # Convert constituency data to a dictionary indexed by number
    constituencies = {}
    for key, value in constituency_data.items():
        constituencies[value['no']] = value
    
    # Create the HTML template
    html_template = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Bihar Assembly Constituencies - Interactive Map</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        
        h1 {
            text-align: center;
            color: #333;
        }
        
        .map-container {
            background-color: white;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            padding: 20px;
            margin-bottom: 20px;
            overflow: auto;
        }
        
        #bihar-map {
            width: 100%;
            height: auto;
        }
        
        #bihar-map path {
            fill: #e0e0e0;
            stroke: #ffffff;
            stroke-width: 1;
            cursor: pointer;
            transition: fill 0.3s ease;
        }
        
        #bihar-map path:hover {
            fill: #bbdefb;
            stroke: #1976d2;
            stroke-width: 2;
        }
        
        #tooltip {
            position: absolute;
            background-color: rgba(0, 0, 0, 0.8);
            color: white;
            padding: 10px;
            border-radius: 4px;
            font-size: 14px;
            pointer-events: none;
            z-index: 1000;
            display: none;
            max-width: 300px;
        }
        
        .controls {
            display: flex;
            justify-content: space-between;
            margin-bottom: 20px;
        }
        
        #search-box {
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 4px;
            width: 300px;
            font-size: 16px;
        }
        
        #selected-info {
            background-color: white;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            padding: 20px;
            margin-top: 20px;
        }
        
        #selected-info h2 {
            margin-top: 0;
            color: #333;
        }
        
        .constituency-list {
            background-color: white;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            padding: 20px;
            margin-top: 20px;
        }
        
        .constituency-list table {
            width: 100%;
            border-collapse: collapse;
        }
        
        .constituency-list th,
        .constituency-list td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }
        
        .constituency-list th {
            background-color: #f2f2f2;
        }
        
        .constituency-list tr:hover {
            background-color: #f5f5f5;
            cursor: pointer;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Bihar Assembly Constituencies</h1>
        
        <div class="controls">
            <input type="text" id="search-box" placeholder="Search constituencies...">
        </div>
        
        <div class="map-container">
            <div id="tooltip"></div>
            <!-- Bihar Map -->
            <div id="bihar-map-container">
                {svg_content}
            </div>
        </div>
        
        <div id="selected-info">
            <h2>Constituency Information</h2>
            <p>Select a constituency from the map or list to view details.</p>
            <div id="constituency-details"></div>
        </div>
        
        <div class="constituency-list">
            <h2>All Constituencies</h2>
            <table id="constituency-table">
                <thead>
                    <tr>
                        <th>No.</th>
                        <th>Name</th>
                        <th>District</th>
                        <th>Reserved</th>
                    </tr>
                </thead>
                <tbody id="constituency-table-body">
                </tbody>
            </table>
        </div>
    </div>

    <script>
        // Constituency data embedded in the HTML
        const constituencyData = {constituency_json};
        
        // Create a mapping from constituency number to data
        const constituencyMap = {};
        for (const key in constituencyData) {
            const constituency = constituencyData[key];
            constituencyMap[constituency.no] = constituency;
        }
        
        // Wait for the DOM to load
        document.addEventListener('DOMContentLoaded', function() {
            // Get the SVG element
            const svgElement = document.querySelector('#bihar-map-container svg');
            if (svgElement) {
                // Set an ID for the SVG element
                svgElement.id = 'bihar-map';
                
                // Get all path elements
                const paths = svgElement.querySelectorAll('path');
                console.log(`Found ${paths.length} path elements`);
                
                // Attach data to paths and add event listeners
                let pathIndex = 1; // Start from 1 as per the plan
                for (const path of paths) {
                    // Skip the first path if it's a background (index 0)
                    if (pathIndex === 1 && path.getAttribute('d') && path.getAttribute('d').length > 1000) {
                        // This is likely the background, skip it
                        console.log('Skipping background path');
                        continue;
                    }
                    
                    const constituency = constituencyMap[pathIndex];
                    if (constituency) {
                        // Set data attributes
                        path.dataset.no = constituency.no;
                        path.dataset.name = constituency.name;
                        path.dataset.district = constituency.district;
                        path.dataset.reserved = constituency.reserved || 'General';
                        
                        // Add title for accessibility
                        const title = document.createElementNS('http://www.w3.org/2000/svg', 'title');
                        title.textContent = `${constituency.no}. ${constituency.name}`;
                        path.appendChild(title);
                        
                        // Add event listeners
                        path.addEventListener('mouseover', function(e) {
                            showTooltip(e, constituency);
                        });
                        
                        path.addEventListener('mousemove', function(e) {
                            moveTooltip(e);
                        });
                        
                        path.addEventListener('mouseout', function() {
                            hideTooltip();
                        });
                        
                        path.addEventListener('click', function() {
                            showConstituencyDetails(constituency);
                        });
                        
                        path.style.cursor = 'pointer';
                    } else {
                        console.warn(`No data found for constituency number ${pathIndex}`);
                    }
                    
                    pathIndex++;
                    
                    // Stop if we've processed all 243 constituencies
                    if (pathIndex > 243) break;
                }
            }
            
            // Populate the constituency table
            populateConstituencyTable(constituencyData);
            
            // Add search functionality
            document.getElementById('search-box').addEventListener('input', function(e) {
                filterConstituencies(e.target.value, constituencyData);
            });
        });
        
        // Tooltip functions
        function showTooltip(e, constituency) {
            const tooltip = document.getElementById('tooltip');
            tooltip.innerHTML = `
                <strong>${constituency.no}. ${constituency.name}</strong><br>
                District: ${constituency.district}<br>
                Type: ${constituency.reserved || 'General'}
            `;
            tooltip.style.display = 'block';
            moveTooltip(e);
        }
        
        function moveTooltip(e) {
            const tooltip = document.getElementById('tooltip');
            tooltip.style.left = (e.pageX + 10) + 'px';
            tooltip.style.top = (e.pageY - 10) + 'px';
        }
        
        function hideTooltip() {
            document.getElementById('tooltip').style.display = 'none';
        }
        
        // Show constituency details
        function showConstituencyDetails(constituency) {
            const detailsContainer = document.getElementById('constituency-details');
            detailsContainer.innerHTML = `
                <h3>${constituency.no}. ${constituency.name}</h3>
                <p><strong>District:</strong> ${constituency.district}</p>
                <p><strong>Constituency Type:</strong> ${constituency.reserved || 'General'}</p>
                <p><strong>Lok Sabha Constituency:</strong> ${constituency.lok_sabha}</p>
                <p><strong>Slug:</strong> ${constituency.slug}</p>
            `;
        }
        
        // Populate constituency table
        function populateConstituencyTable(constituencyData) {
            const tableBody = document.getElementById('constituency-table-body');
            tableBody.innerHTML = '';
            
            // Convert object to array and sort by constituency number
            const constituencies = Object.values(constituencyData).sort((a, b) => a.no - b.no);
            
            constituencies.forEach(constituency => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${constituency.no}</td>
                    <td>${constituency.name}</td>
                    <td>${constituency.district}</td>
                    <td>${constituency.reserved || 'General'}</td>
                `;
                
                row.addEventListener('click', function() {
                    showConstituencyDetails(constituency);
                    
                    // Scroll to details
                    document.getElementById('selected-info').scrollIntoView({ behavior: 'smooth' });
                });
                
                tableBody.appendChild(row);
            });
        }
        
        // Filter constituencies based on search term
        function filterConstituencies(searchTerm, constituencyData) {
            const tableBody = document.getElementById('constituency-table-body');
            tableBody.innerHTML = '';
            
            // Convert object to array and sort by constituency number
            const constituencies = Object.values(constituencyData)
                .sort((a, b) => a.no - b.no)
                .filter(constituency => 
                    constituency.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                    constituency.district.toLowerCase().includes(searchTerm.toLowerCase())
                );
            
            constituencies.forEach(constituency => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${constituency.no}</td>
                    <td>${constituency.name}</td>
                    <td>${constituency.district}</td>
                    <td>${constituency.reserved || 'General'}</td>
                `;
                
                row.addEventListener('click', function() {
                    showConstituencyDetails(constituency);
                    
                    // Scroll to details
                    document.getElementById('selected-info').scrollIntoView({ behavior: 'smooth' });
                });
                
                tableBody.appendChild(row);
            });
        }
    </script>
</body>
</html>'''
    
    # Embed the SVG content and JSON data in the template
    # Escape the SVG content for use in HTML
    svg_escaped = svg_content.replace('`', '\\`').replace('${', '\\${')
    constituency_json = json.dumps(constituencies)
    
    return html_template.format(svg_content=svg_content, constituency_json=constituency_json)

def main():
    # File paths
    svg_path = 'Bihar_const.svg'
    json_path = 'bihar_constituencies.json'
    output_path = 'bihar_assembly_map.html'
    
    # Read the files
    svg_content = read_svg_file(svg_path)
    constituency_data = read_json_file(json_path)
    
    # Create the interactive map
    html_content = create_interactive_map(svg_content, constituency_data)
    
    # Write the HTML file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"Interactive map created successfully: {output_path}")

if __name__ == '__main__':
    main()