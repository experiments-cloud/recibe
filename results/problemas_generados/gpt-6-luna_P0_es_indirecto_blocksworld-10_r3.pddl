(define (problem bloques)
  (:domain BLOCKS)
  (:objects
    a - block
    b - block
    c - block
    d - block
    e - block
    f - block
    g - block
    h - block
  )
  (:init
    (on a g)
    (on g e)
    (ontable e)
    (clear a)
    (on d h)
    (on h f)
    (ontable f)
    (clear d)
    (ontable b)
    (clear b)
    (ontable c)
    (clear c)
    (handempty)
  )
  (:goal
    (and
      (on d f)
      (on f e)
      (on e h)
      (on h c)
      (on c a)
      (on a g)
      (on g b)
    )
  )
)
