import { Table, useMantineTheme, useComputedColorScheme, Paper, Grid } from "@mantine/core"


export const TableauEditor = ({size}: {size : number})  => {
    const computedColorScheme = useComputedColorScheme('light', { getInitialValueInEffect: true });
    console.log("Component is rendering..."); 
    return (
        <>
            <div>
                
    
                    {[...Array(size)].map((_,index) => (
                        <Grid key={`row-${index}`} gap={0}>
                            {[...Array(size-index)].map((_,j) => (
                                <Paper key={`cell-${index}-${j}`} radius="xs" className={`hover:bg-gray-300/70 border border-gray-300 items-center justify-center`}>j</Paper> 
                            ))}
                        </Grid>
                    
                    ))}
            
            </div>


        </>
    )
}