import { Table, useMantineTheme,ScrollArea,SimpleGrid , Box, useComputedColorScheme, Paper, Grid, Text } from "@mantine/core"


export const TableauEditor = ({size}: {size : number})  => {
    const computedColorScheme = useComputedColorScheme('light', { getInitialValueInEffect: true });
    console.log("Component is rendering..."); 
    return (
        <>
            <ScrollArea w="100%">
                <div  style={{ minWidth: 400}} >
    
                    {[...Array(size+1)].map((_,index) => (
                        
                        <Grid key={`row-${index}`} w="100%"gap={0} overflow='hidden'>

                            {[...Array(size-index)].map((_,j) => (
                                <>
                                {
                                !(index == 0 && j == size-1)
                                &&
                                !(index == size - 1)
                                &&
                                <Box 
                                key={`cell-${index}-${j}`} 
                                className={`hover:bg-gray-300/70 border-[0.4]
                                    ${index == 0 && 'border-t-0 border-x-0 hover:bg-none'}
                                    ${j == 0 && 'border-l-0 border-y-0 hover:bg-none'}
                                    
                                    ${ index == size-1 ? 'rounded-bl-xs' : ''} 
                                    ${ j == size-index-1 ? 'rounded-br-xs' : ''}
                                    ${ index == 0 && j == size-index-1? 'rounded-tr-xs' : ''} 
                                    ${ index == 0 && j == 0? 'rounded-tl-xs' : ''} 
                                     border-gray-300/40 size-[4vw] min-w-7 min-h-7 max-w-10 max-h-10 items-center-safe`} 
                                    style={{ justifyContent: 'center', alignItems: 'center' }}>
                                    <Box ta="center" h="100%" w="100%">
                                    j
                                    </Box>
                                </Box>
                                }
                                </>
                            ))}
                        </Grid>
                    
                    ))}
                </div >
            </ScrollArea>


        </>
    )
}