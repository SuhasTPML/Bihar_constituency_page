#!/usr/bin/env node

/**
 * GeoJSON Cleanup Script
 * Removes unused properties from bihar_ac_all.geojson to reduce file size
 */

const fs = require('fs');
const path = require('path');

// File paths
const INPUT_FILE = 'bihar_ac_all.geojson';
const OUTPUT_FILE = 'bihar_ac_all_optimized.geojson';

// Properties to keep (all others will be removed)
const KEEP_PROPERTIES = [
  'AC_NO',
  'AC_NAME',
  'DIST_NAME',
  'PC_NO',
  'PC_NAME'
];

console.log('🧹 GeoJSON Cleanup Script');
console.log('========================\n');

// Read the input file
console.log(`📖 Reading: ${INPUT_FILE}`);
let inputData = fs.readFileSync(INPUT_FILE, 'utf8');

// Remove BOM if present
if (inputData.charCodeAt(0) === 0xFEFF) {
  console.log('   Removing BOM (Byte Order Mark)...');
  inputData = inputData.slice(1);
}

const inputSize = Buffer.byteLength(inputData, 'utf8');
console.log(`   Size: ${(inputSize / 1024 / 1024).toFixed(2)} MB`);

// Parse JSON
console.log('⚙️  Parsing JSON...');
const geoJson = JSON.parse(inputData);

// Validate structure
if (!geoJson.features || !Array.isArray(geoJson.features)) {
  console.error('❌ Invalid GeoJSON structure');
  process.exit(1);
}

console.log(`   Features: ${geoJson.features.length}`);

// Clean up properties
console.log('🔧 Removing unused properties...');
let removedCount = 0;
const propertiesSample = geoJson.features[0].properties;
const originalKeys = Object.keys(propertiesSample);

geoJson.features.forEach((feature, index) => {
  const cleanedProperties = {};

  KEEP_PROPERTIES.forEach(prop => {
    if (feature.properties.hasOwnProperty(prop)) {
      cleanedProperties[prop] = feature.properties[prop];
    }
  });

  const beforeCount = Object.keys(feature.properties).length;
  const afterCount = Object.keys(cleanedProperties).length;
  removedCount += (beforeCount - afterCount);

  feature.properties = cleanedProperties;
});

console.log(`   Properties before: ${originalKeys.length}`);
console.log(`   Properties after: ${KEEP_PROPERTIES.length}`);
console.log(`   Removed per feature: ${originalKeys.length - KEEP_PROPERTIES.length}`);
console.log(`   Total properties removed: ${removedCount}`);

// Removed properties summary
const removedProps = originalKeys.filter(key => !KEEP_PROPERTIES.includes(key));
console.log(`\n   Removed: ${removedProps.join(', ')}`);
console.log(`   Kept: ${KEEP_PROPERTIES.join(', ')}`);

// Write output file
console.log(`\n💾 Writing: ${OUTPUT_FILE}`);
const outputData = JSON.stringify(geoJson, null, 2);
fs.writeFileSync(OUTPUT_FILE, outputData, 'utf8');

const outputSize = Buffer.byteLength(outputData, 'utf8');
console.log(`   Size: ${(outputSize / 1024 / 1024).toFixed(2)} MB`);

// Calculate savings
const savings = inputSize - outputSize;
const savingsPercent = ((savings / inputSize) * 100).toFixed(2);

console.log('\n📊 Results:');
console.log(`   Original size: ${(inputSize / 1024 / 1024).toFixed(2)} MB`);
console.log(`   Optimized size: ${(outputSize / 1024 / 1024).toFixed(2)} MB`);
console.log(`   Saved: ${(savings / 1024 / 1024).toFixed(2)} MB (${savingsPercent}%)`);

console.log('\n✅ Done! File saved as:', OUTPUT_FILE);
console.log('\nNext steps:');
console.log('1. Test the optimized file with your map');
console.log('2. If it works, replace the original:');
console.log(`   mv ${OUTPUT_FILE} ${INPUT_FILE}`);
